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

The dataset is downloaded with a script, see `scripts/download_data.py`
(added in a later step). Images are never committed to this repository.

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
