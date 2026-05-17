#!/usr/bin/env python3
"""
qdpdb_parser.py -- Python parser for Chroma qdpdb (FILEDB / FFDB) binary files.

================================================================================
W1B Phase E2 lattice extraction (2026-05-17)
================================================================================

PURPOSE
-------
Chroma's INLINE_GLUEBALL_OPS measurement writes one binary qdpdb file per
gauge configuration and APE smearing level.  These are FILEDB-format hash
database files (Edwards/Chen, Jefferson Lab; magic 0xcece3434, version 5).
Per-file content:

    pages 0    -- file header  (24 bytes + slot dir)
    pages 1-2  -- DBMetaData (XML) + user info
    pages 3-N  -- hash-bucket pages (small KEY records pointing to overflow)
    pages N+1+ -- data-overflow pages (1 complex<double> per record, FFDB EMBED)

Each key is one tuple (t_slice, op_signature) where op_signature is a sequence
of small integers identifying the elemental glueball operator path (the
exact mapping is set in chroma/lib/meas/glue/inline_glueball_ops.cc).  Each
value is one complex<double> stored big-endian.

LIMITATIONS  (READ BEFORE USING)
--------------------------------
*  Header / page-flag interpretation reverse-engineered from binary; we DO
   NOT have access to the chroma `inline_glueball_ops` source on this host,
   so we treat key_ints[0] as the timeslice (verified empirically: each
   distinct op-signature yields exactly 16 keys, one per t in [0..15]) and
   key_ints[1:] as an opaque operator signature.
*  Multiple overflow pages may map the SAME logical key to several stored
   complex values.  We currently keep the union and let the caller decide
   (`parse_qdpdb` returns ALL records per key).  In typical files the page-35
   value is the physically meaningful one; pages 36-37 hold internal-state
   overlap terms that should be averaged into the same correlator element.
*  We do NOT recover the human-readable (op_i, op_j) labels.  GEVP analysis
   that requires explicit identification of plaquette/rectangle/etc. shapes
   must be done with Chroma's own utilities on the original host.

The parser is sufficient to
    (a) read all complex correlator entries from any qdpdb file produced by
        chroma>=3.44 with INLINE_GLUEBALL_OPS;
    (b) recover the embedded DBMetaData XML (latt_size, beta, run_date, etc.);
    (c) extract the t-dependence of each operator signature for diagnostic
        plots of effective masses (provided one accepts the unlabeled
        signature scheme above).

REFERENCES
----------
- arXiv:hep-lat/0404008  Lucini, Teper, Wenger 2004, glueball ops basis;
                         VERIFIED_LIVE 2026-05-17.
- arXiv:2106.00364       Athenodorou, Teper 2021, AT 2021 SOTA SU(N) glueball;
                         VERIFIED_LIVE 2026-05-17.
- qdpxx headers in /root/install/qdpxx/include/{qdp_db_imp.h,ffdb_db.h,
  DBKey.h,DBData.h,ConfDataStoreDB.h}.

Author: Claude (Opus 4.7 1M ctx), 2026-05-17.  No persona, no fabricated IDs.
"""

from __future__ import annotations
import struct
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Iterable, Any
from collections import defaultdict


PAGE_SIZE = 8192                 # FFDB default page size for these files
FFDB_MAGIC = 0xCECE3434          # ffdb_db.h:191
FFDB_STORE_EMBED = 0xFFEEFFEE    # data-record marker actually observed
                                 # (ffdb_db.h has 0x00FFDDEE, byte order differs)

# Hash-page flags observed in the wild: lower byte is the page "type".
HASH_PAGE_TYPES = {0x09, 0x0C, 0x0F, 0x12, 0x15, 0x18}
# Overflow-data page low-byte flags
DATA_PAGE_TYPE_MASK = 0xCC        # observed 0xCC for full data pages
DATA_PAGE_TYPE_TAIL = 0x18        # observed 0x18 for tail (partial) page


# =============================================================================
# 1. KEY RECORD (lives on hash-bucket pages)
# =============================================================================
@dataclass
class Key:
    """One key record from a hash-bucket page."""
    src_pg: int                   # which page this key was found on
    src_pos: int                  # byte offset in file
    ksize: int                    # key size (35 or 36 bytes for glueballOps)
    data_off: int                 # offset within target page where data lives
    data_pg: int                  # target page number (logical, see notes)
    hash_or_chk: int              # 4-byte hash/checksum (used for collision)
    key_ints: Tuple[int, ...]     # decoded big-endian uint32 sequence

    @property
    def t_slice(self) -> int:
        """Conjectured timeslice (key_ints[0]).  Verified empirically: each
        unique tuple key_ints[1:] yields exactly 16 keys with key_ints[0]
        spanning {0..Lt-1}."""
        return self.key_ints[0]

    @property
    def op_signature(self) -> Tuple[int, ...]:
        """Operator signature.  All bytes after timeslice."""
        return self.key_ints[1:]


# =============================================================================
# 2. DATA RECORD (lives on overflow pages)
# =============================================================================
@dataclass
class DataRecord:
    """One value record on an overflow page (EMBED-storage of complex<double>)."""
    src_pg: int
    src_pos: int
    rec_off: int                  # offset within page (== Key.data_off for match)
    bucket: int                   # hash bucket index (NOT timeslice!)
    re: float                     # real part (big-endian double)
    im: float                     # imaginary part (big-endian double)

    @property
    def value(self) -> complex:
        return complex(self.re, self.im)


# =============================================================================
# 3. FILE HEADER + METADATA
# =============================================================================
@dataclass
class FileDBHeader:
    magic: int                    # should be 0xcece3434
    version: int                  # should be 5
    secret: int                   # observed 0x4d2
    pagesize: int                 # observed 0x2000
    num_pages: int                # total pages in file
    nbuckets: int                 # hash table size
    user_info_len: int
    metadata_xml: Optional[str]   # extracted DBMetaData XML
    latt_size: Optional[Tuple[int, int, int, int]]
    beta: Optional[float]
    run_date: Optional[str]


def read_header(data: bytes) -> FileDBHeader:
    """Parse the FILEDB header (first 64 bytes) and recover DBMetaData XML."""
    if len(data) < 64:
        raise ValueError("qdpdb file too small")
    if struct.unpack('>I', data[0:4])[0] != FFDB_MAGIC:
        raise ValueError(f"bad magic 0x{struct.unpack('>I', data[0:4])[0]:x}; "
                         f"expected 0x{FFDB_MAGIC:x}")
    version = struct.unpack('>I', data[4:8])[0]
    secret  = struct.unpack('>I', data[8:12])[0]
    pgsz    = struct.unpack('>I', data[12:16])[0]
    nb      = struct.unpack('>I', data[16:20])[0]   # 0x0d typical
    # ... other fields skipped, format isn't fully documented in public header
    num_pages = len(data) // pgsz

    # DBMetaData lives on page 1, starting after a small page header.
    pg1_start = pgsz
    xml_start = data.find(b'<?xml', pg1_start, pg1_start + pgsz)
    xml_end = data.find(b'</DBMetaData>', xml_start) if xml_start >= 0 else -1
    xml = None
    latt = beta = run_date = None
    if xml_start >= 0 and xml_end > xml_start:
        xml = data[xml_start:xml_end+len(b'</DBMetaData>')].decode('utf-8',
                                                                 errors='replace')
        m = re.search(r'<lattSize>\s*([\d ]+)\s*</lattSize>', xml)
        if m:
            try:
                vals = tuple(int(x) for x in m.group(1).split())
                if len(vals) == 4:
                    latt = vals
            except ValueError:
                pass
        m = re.search(r'<beta>\s*([\d.eE+\-]+)\s*</beta>', xml)
        if m:
            try:
                beta = float(m.group(1))
            except ValueError:
                pass
        m = re.search(r'<run_date>\s*([^<]+)\s*</run_date>', xml)
        if m:
            run_date = m.group(1).strip()

    return FileDBHeader(
        magic=FFDB_MAGIC, version=version, secret=secret,
        pagesize=pgsz, num_pages=num_pages, nbuckets=nb,
        user_info_len=0,
        metadata_xml=xml, latt_size=latt, beta=beta, run_date=run_date,
    )


# =============================================================================
# 4. PAGE WALKER -- extract keys and data records
# =============================================================================
def _page_flags(data: bytes, pg_off: int) -> int:
    return struct.unpack('<I', data[pg_off+16:pg_off+20])[0]


def _page_free_offset(data: bytes, pg_off: int) -> int:
    return struct.unpack('<I', data[pg_off+24:pg_off+28])[0]


def _extract_keys_from_page(data: bytes, pg_idx: int) -> List[Key]:
    pg_off = pg_idx * PAGE_SIZE
    if pg_off + PAGE_SIZE > len(data):
        return []
    flags = _page_flags(data, pg_off)
    if (flags & 0xFF) not in HASH_PAGE_TYPES:
        return []
    free_off = _page_free_offset(data, pg_off)
    if free_off == 0 or free_off >= PAGE_SIZE:
        return []
    # Records fill from free_off+1 to end of page (with 4-byte alignment).
    pos = pg_off + free_off + 1
    out: List[Key] = []
    while pos + 16 < pg_off + PAGE_SIZE:
        try:
            ksize = struct.unpack('<I', data[pos:pos+4])[0]
        except struct.error:
            break
        if ksize not in (35, 36):
            pos += 4
            continue
        d_off = struct.unpack('<I', data[pos+4:pos+8])[0]
        d_pg  = struct.unpack('<I', data[pos+8:pos+12])[0]
        d_chk = struct.unpack('<I', data[pos+12:pos+16])[0]
        key_bytes = data[pos+16:pos+16+ksize]
        if len(key_bytes) < ksize:
            break
        n_ints = ksize // 4
        key_ints = struct.unpack(f'>{n_ints}I', key_bytes[:n_ints * 4])
        out.append(Key(
            src_pg=pg_idx, src_pos=pos, ksize=ksize,
            data_off=d_off, data_pg=d_pg, hash_or_chk=d_chk,
            key_ints=key_ints,
        ))
        # Advance past the record, then to next 4-byte boundary.
        pos += 16 + ksize
        pad = (4 - ((16 + ksize) % 4)) % 4
        pos += pad
    return out


def _extract_data_from_page(data: bytes, pg_idx: int) -> List[DataRecord]:
    pg_off = pg_idx * PAGE_SIZE
    if pg_off + PAGE_SIZE > len(data):
        return []
    flags = _page_flags(data, pg_off)
    # We accept any page whose body holds the EMBED magic; tail pages are
    # partially filled but their first records are still valid.
    out: List[DataRecord] = []
    pos = pg_off + 24
    page_end = min(pg_off + PAGE_SIZE, len(data))
    while pos + 40 <= page_end:
        magic = struct.unpack('<I', data[pos+4:pos+8])[0]
        if magic == FFDB_STORE_EMBED:
            rec_off = struct.unpack('<I', data[pos+8:pos+12])[0]
            bucket  = struct.unpack('<I', data[pos+12:pos+16])[0]
            re      = struct.unpack('>d', data[pos+24:pos+32])[0]
            im      = struct.unpack('>d', data[pos+32:pos+40])[0]
            out.append(DataRecord(
                src_pg=pg_idx, src_pos=pos,
                rec_off=rec_off, bucket=bucket, re=re, im=im,
            ))
            pos += 40
        else:
            pos += 4
    return out


# =============================================================================
# 5. PUBLIC API
# =============================================================================
@dataclass
class ParsedQdpdb:
    header: FileDBHeader
    keys: List[Key]                                    # all hash-bucket entries
    data: List[DataRecord]                             # all data records
    # Map (target_page, byte_offset) -> [DataRecord, ...]
    by_offset: Dict[Tuple[int, int], List[DataRecord]] = field(default_factory=dict)
    # Map key_ints tuple -> list of complex values pulled by data_off
    keyed_values: Dict[Tuple[int, ...], List[complex]] = field(default_factory=dict)


def parse_qdpdb(path: str | Path, *, verbose: bool = False) -> ParsedQdpdb:
    """Parse a single Chroma qdpdb file.

    Returns a ParsedQdpdb with:
      - header             : file metadata (magic, version, latt_size, beta, run_date)
      - keys               : list of Key   (one per (t, op_signature))
      - data               : list of DataRecord (one per complex<double> stored)
      - keyed_values       : {key_ints_tuple : [complex, ...]} convenience map

    Caller responsibilities:
      - To get a correlator C[t] for a chosen op_signature s, gather all
        records with key.op_signature == s and index by key.t_slice.
      - Multiple data records may match one key (overflow paging): the caller
        should sum or average as appropriate (typically the first matching
        record's value is the physical correlator entry).
    """
    path = Path(path)
    with open(path, 'rb') as fh:
        data = fh.read()
    if len(data) < 64:
        raise ValueError(f"{path}: too small to be a qdpdb file")

    header = read_header(data)
    if verbose:
        print(f"[qdpdb] {path.name}: magic OK, version={header.version}, "
              f"pages={header.num_pages}, latt={header.latt_size}, "
              f"beta={header.beta}")

    # Walk pages 3..N-1 for keys, then pages with data flags for values.
    keys: List[Key] = []
    data_records: List[DataRecord] = []
    for pg_idx in range(3, header.num_pages):
        ks = _extract_keys_from_page(data, pg_idx)
        if ks:
            keys.extend(ks)
            continue
        # Not a key-bucket page -- maybe an overflow data page.
        drs = _extract_data_from_page(data, pg_idx)
        if drs:
            data_records.extend(drs)

    by_offset: Dict[Tuple[int, int], List[DataRecord]] = defaultdict(list)
    for r in data_records:
        by_offset[(r.src_pg, r.rec_off)].append(r)

    # Build keyed_values by following key.data_off to ALL overflow records
    # at that byte offset (across any data page).
    by_off_only: Dict[int, List[DataRecord]] = defaultdict(list)
    for r in data_records:
        by_off_only[r.rec_off].append(r)

    keyed_values: Dict[Tuple[int, ...], List[complex]] = {}
    for k in keys:
        matching = by_off_only.get(k.data_off, [])
        keyed_values[k.key_ints] = [r.value for r in matching]

    if verbose:
        # Op-signature statistics
        sigs = defaultdict(int)
        for k in keys:
            sigs[k.op_signature] += 1
        full_sigs = sum(1 for v in sigs.values() if v == 16)
        print(f"[qdpdb] {len(keys)} keys, {len(data_records)} data records, "
              f"{len(sigs)} op_signatures ({full_sigs} with all 16 timeslices).")

    return ParsedQdpdb(
        header=header, keys=keys, data=data_records,
        by_offset=dict(by_offset), keyed_values=keyed_values,
    )


# =============================================================================
# 6. CONVENIENCE: extract per-signature C[t]
# =============================================================================
def correlator_by_signature(parsed: ParsedQdpdb,
                            *, value_selector: str = "first"
                            ) -> Dict[Tuple[int, ...], List[complex]]:
    """Group records into  {op_signature : [C(t=0), C(t=1), ..., C(t=Lt-1)]}.

    value_selector controls how multi-page hits are reduced:
      "first" -- take only the first matching record (typically physical)
      "sum"   -- sum all matches
      "mean"  -- arithmetic mean of all matches
    """
    by_sig: Dict[Tuple[int, ...], Dict[int, complex]] = defaultdict(dict)
    for k in parsed.keys:
        vals = parsed.keyed_values.get(k.key_ints, [])
        if not vals:
            continue
        if value_selector == "first":
            v = vals[0]
        elif value_selector == "sum":
            v = sum(vals)
        elif value_selector == "mean":
            v = sum(vals) / len(vals)
        else:
            raise ValueError(f"unknown value_selector={value_selector!r}")
        by_sig[k.op_signature][k.t_slice] = v

    out: Dict[Tuple[int, ...], List[complex]] = {}
    for sig, tmap in by_sig.items():
        if not tmap:
            continue
        Lt = max(tmap) + 1
        out[sig] = [tmap.get(t, complex(float("nan"), float("nan"))) for t in range(Lt)]
    return out


# =============================================================================
# 7. CLI for quick inspection
# =============================================================================
def _cli(argv: List[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    paths = [Path(p) for p in argv]
    for p in paths:
        if not p.is_file():
            print(f"[err] missing file: {p}", file=sys.stderr)
            continue
        parsed = parse_qdpdb(p, verbose=True)
        if parsed.header.metadata_xml:
            beta = parsed.header.beta
            latt = parsed.header.latt_size
            print(f"  beta={beta!r}  latt={latt!r}")
        # Show a few signatures and their values
        cor = correlator_by_signature(parsed, value_selector="first")
        sig_sizes = sorted([(s, len(c)) for s, c in cor.items()], key=lambda x: -x[1])
        for sig, _ in sig_sizes[:3]:
            vals = cor[sig]
            mod = [abs(v) for v in vals]
            print(f"  sig={sig}:  max|C|={max(mod):.3e}  |C(0)|={mod[0]:.3e}  "
                  f"|C(Lt//2)|={mod[len(mod)//2]:.3e}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
