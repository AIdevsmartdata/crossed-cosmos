# AWS spot launch — ECI v4/v5 MCMC

One-page owner walkthrough. Region: **eu-west-3 (Paris)**. No Terraform required
(a manual path is given; optional Terraform stub at the bottom).

## 0. Prereqs (once)

- AWS account with a billing alert at **$20** (AWS Budgets → *Create budget* →
  *Cost budget*, monthly $20, email alert at 80 %).
- IAM user or SSO role with: `EC2FullAccess`, `IAMReadOnlyAccess`,
  `AmazonS3FullAccess` (scoped to the target bucket, e.g. `eci-mcmc-<owner>`).
- Local `aws` CLI configured: `aws configure --profile eci` (region
  `eu-west-3`).
- S3 bucket for chain artefacts:
  ```bash
  aws --profile eci s3 mb s3://eci-mcmc-<owner> --region eu-west-3
  ```

## 1. Spot price check

```bash
aws --profile eci ec2 describe-spot-price-history \
    --instance-types c7i.24xlarge \
    --product-descriptions 'Linux/UNIX' \
    --max-results 5 \
    --region eu-west-3
```

Typical eu-west-3 spot price early 2026: **$0.90 – $1.30 / h** (on-demand is
≈ $4.28/h). Abort if spot > $2.00/h.

## 2. Launch the instance

- **AMI**: *Deep Learning Base AMI (Ubuntu 22.04)* — Docker Engine, NVIDIA
  drivers (unused here), and OpenMPI come pre-installed.
  ```bash
  aws --profile eci ec2 describe-images \
      --owners amazon \
      --filters 'Name=name,Values=Deep Learning Base GPU AMI (Ubuntu 22.04)*' \
      --query 'sort_by(Images,&CreationDate)[-1].[ImageId,Name]' \
      --region eu-west-3
  ```
- **Instance type**: `c7i.24xlarge` — 96 vCPU Intel Sapphire Rapids, 192 GiB RAM.
- **Root volume**: 150 GiB gp3 (Planck + ACT data ≈ 5 GB, chains ≈ 1 GB).
- **Spot options**: *persistent* request is discouraged (cost creep); use a
  one-time request with max price $2.00/h.
- **Key pair**: your personal SSH key.
- **Security group**: inbound 22/tcp from your IP only; all outbound.

Console path: *EC2 → Launch Instance → Advanced → Request Spot Instances*.
Or CLI:

```bash
aws --profile eci ec2 run-instances \
    --image-id <AMI_ID> \
    --instance-type c7i.24xlarge \
    --key-name <YOUR_KEY> \
    --security-group-ids <SG_ID> \
    --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=150,VolumeType=gp3}' \
    --instance-market-options 'MarketType=spot,SpotOptions={MaxPrice=2.00,SpotInstanceType=one-time}' \
    --iam-instance-profile 'Name=eci-s3-writer' \
    --region eu-west-3 \
    --count 1
```

(`eci-s3-writer` = instance profile with `s3:PutObject` on the bucket.)

## 3. Provision & run

```bash
ssh -i ~/.ssh/<key>.pem ubuntu@<PUBLIC_DNS>

# Clone repo
git clone https://github.com/<owner>/crossed-cosmos.git
cd crossed-cosmos

# Build image (~ 8 min, ~ 2.5 GB)
docker build -t eci-mcmc:v5 -f mcmc/deploy/Dockerfile .

# Run — bind-mount repo, separate volume for cobaya `packages/` (5 GB data)
docker volume create eci_packages
docker run --rm -it \
    -v "$PWD":/opt/eci \
    -v eci_packages:/opt/eci/mcmc/packages \
    -e S3_BUCKET=eci-mcmc-<owner> \
    -e NCHAINS=4 \
    -e OMP_NUM_THREADS=24 \
    --name eci-run \
    eci-mcmc:v5
```

`mpirun -np 4 × OMP 24 = 96 vCPU` → full utilisation of the instance.

## 4. Wall-clock & cost

| Phase                              | Time      | Notes                                   |
|------------------------------------|-----------|-----------------------------------------|
| `cobaya-install cosmo`             | 20 min    | One-shot download (~5 GB).              |
| Warm-up + proposal learning        | 45 min    | Cobaya `learn_proposal`.                |
| Sampling to R-1 < 0.05             | 5 – 6 h   | ~ 80 k accepted steps / chain.          |
| Tar + S3 upload                    | 5 min     |                                         |
| **Total**                          | **~ 7 h** | c7i.24xlarge is ≈ 8× faster than i5-14600KF. |

Spot cost: `7 h × $1.10/h ≈ $7.70`. Budget ceiling **$8 – $15 per run**;
alert at **$20** via AWS Budgets.

## 5. Spot-interruption fallback

Cobaya writes `.checkpoint` and progress files every few hundred steps (its
default behaviour — no extra config needed). On interruption:

1. New spot request (same AMI, new volume attach if ephemeral EBS lost).
2. `docker run … eci-mcmc:v5` with the **same** `eci_packages` volume and a
   bind-mount of the repo whose `mcmc/chains/` dir is restored from S3.
3. `run_mcmc.sh` calls `cobaya-run -r` → resumes in place.

To survive full instance loss, export chains to S3 on a 30 min cron inside the
container:

```bash
docker exec eci-run bash -lc \
  "while true; do aws s3 sync /opt/eci/mcmc/chains s3://eci-mcmc-<owner>/live/; sleep 1800; done" &
```

## 6. Teardown

```bash
aws --profile eci ec2 terminate-instances --instance-ids <I-ID> --region eu-west-3
aws --profile eci ec2 cancel-spot-instance-requests --spot-instance-request-ids <SIR-ID> --region eu-west-3
```

Verify: `aws ec2 describe-instances --instance-ids <I-ID>` → state `terminated`.
The EBS root volume is deleted on terminate (default `DeleteOnTermination=true`).
The S3 bucket persists; lifecycle rule `eci_mcmc/ → Glacier after 30 d` is
recommended to cap storage cost.

### Optional: Terraform

A 40-line `main.tf` in this folder (not committed — owner preference) can wrap
the above: `terraform apply` to launch, `terraform destroy` to tear down. The
manual CLI path above is authoritative.

## 7. Manual checklist before first run

- [ ] S3 bucket created in eu-west-3.
- [ ] AWS Budgets alert at $20 armed.
- [ ] IAM instance profile `eci-s3-writer` attached to the instance.
- [ ] `mcmc/params/eci_nmc.yaml` validated locally via
      `python mcmc/deploy/eci_nmc_yaml_validator.py` (exit 0).
- [ ] NMC theory route decided (hi_class C patch **or** Cobaya plugin) and the
      YAML `theory:` block matches.
- [ ] Planck 2018 likelihood EULA accepted (cobaya-install will prompt once).
