# neumre-anomaly-detection

Visual product quality control with neural networks. Team project for the
Neural Networks course (NEUMRE) at FER Zagreb, Team 11.

We detect and localize visible defects on product images when only images of
defect-free products are available for training. Models are trained only on
good images from the MVTec AD dataset and must flag anything that differs from
them, both per image and per pixel. We compare three variants: (A) a
convolutional autoencoder, (B) a denoising autoencoder and (C) a small U-Net
trained to segment synthetic defects. We use three categories: bottle,
hazelnut and tile.

## Setup

Requires Python 3.11.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Repository layout

```
src/neumre/   Python package with shared code
scripts/      command-line scripts (data download, checks)
notebooks/    Jupyter notebooks for exploration
configs/      experiment configuration files
data/         dataset (not committed, see data/README.md)
outputs/      checkpoints, logs and results (not committed)
reports/      project report and presentation
```

## Data

We use the Kaggle copy of the dataset,
[ipythonx/mvtec-ad](https://www.kaggle.com/datasets/ipythonx/mvtec-ad).
Images and archives are never committed to this repository.

### On Kaggle Notebooks (main setup)

We train in Kaggle Notebooks, so no download is needed:

1. In the notebook, click *Add Input* and add the dataset
   `ipythonx/mvtec-ad`. It appears under `/kaggle/input/` (for example
   `/kaggle/input/mvtec-ad/bottle/`).
2. Turn on *Internet* in the notebook settings, then get the code:

   ```bash
   !git clone https://github.com/karlalucic/neumre-anomaly-detection.git
   %cd neumre-anomaly-detection
   !pip install -q -r requirements.txt
   ```

3. Use the attached folder as the dataset folder instead of `data/mvtec_ad`.

Save checkpoints and results under `/kaggle/working/`. That folder is kept
when the notebook version is saved.

### Locally or on Colab

Use `scripts/download_data.py`. It needs a Kaggle API token.

#### 1. Get a Kaggle API token

1. Log in to [kaggle.com](https://www.kaggle.com) and open
   *Settings → API*.
2. Click *Create New Token*. Depending on the page, you get either a
   `kaggle.json` file or a token string.
3. Store it in one of these places (never inside this repository):
   - `kaggle.json`: move it to `~/.kaggle/kaggle.json` and run
     `chmod 600 ~/.kaggle/kaggle.json`.
   - Token string: save it to `~/.kaggle/access_token`, or set
     `export KAGGLE_API_TOKEN=<token>`.
   - Or set `export KAGGLE_USERNAME=<username>` and `export KAGGLE_KEY=<key>`.

#### 2. Download

```bash
python scripts/download_data.py
```

The script downloads the full archive once (about 5 GB), extracts only bottle,
hazelnut and tile into `data/mvtec_ad/<category>/` and deletes the archive.
You need about 6 GB of free disk space during the download. Categories that
are already present are skipped, so the script is safe to run again.

### Credit

We use the MVTec AD dataset:

P. Bergmann, K. Batzner, M. Fauser, D. Sattlegger and C. Steger, "The MVTec
Anomaly Detection Dataset: A Comprehensive Real-World Dataset for Unsupervised
Anomaly Detection", *International Journal of Computer Vision*, 129,
1038–1059, 2021.

The dataset is licensed under CC BY-NC-SA 4.0. We use it for educational
purposes only.

## License

Our code is released under the MIT License, see `LICENSE`. The MVTec AD
dataset is not covered by this license and keeps its own license
(CC BY-NC-SA 4.0).
