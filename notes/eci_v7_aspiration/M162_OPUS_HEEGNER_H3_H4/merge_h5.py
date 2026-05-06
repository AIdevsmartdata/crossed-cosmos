#!/usr/bin/env python3
"""Merge 08_h5_results.json into 04_results.json (only entries not already present)."""
import json

with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results.json') as f:
    main = json.load(f)
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/08_h5_results.json') as f:
    h5 = json.load(f)

main_keys = set((r['D'], r['j']) for r in main)
added = 0
for r in h5:
    key = (r['D'], r['j'])
    if key not in main_keys:
        main.append(r)
        main_keys.add(key)
        added += 1

# Save merged (do NOT overwrite if 06 is running — instead write to a new file we'll merge later)
with open('/root/crossed-cosmos/notes/eci_v7_aspiration/M162_OPUS_HEEGNER_H3_H4/04_results_merged.json', 'w') as f:
    json.dump(main, f, indent=2, default=str)
print(f"Added {added} h=5 entries; total {len(main)}; saved to 04_results_merged.json")
