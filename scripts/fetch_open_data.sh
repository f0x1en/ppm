#!/bin/sh
# Download open datasets used by the notebooks into ext/ (not tracked by git).
# Malani et al., Cancer Discov 2022; Zenodo 10.5281/zenodo.7370747; CC BY 4.0.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
mkdir -p ext/malani2022
cd ext/malani2022
[ -f data.zip ] || curl -fL -o data.zip "https://zenodo.org/api/records/7370747/files/Functional_Precision_Medicine_Tumor_Board_AML.zip/content"
echo "expected size 38810683 bytes, got $(wc -c < data.zip)"
unzip -oq data.zip
ls -R | head -40

# DECREASE (Ianevski et al., Nat Mach Intell 2019): 192 measured 8x8 combination matrices. Code GPL-3; data used read-only.
cd "$ROOT"
[ -d ext/decrease ] || git clone -q https://github.com/IanevskiAleksandr/DECREASE.git ext/decrease
git -C ext/decrease checkout -q 0f5871cad64fb8c43a88242e02baac175ed98d0e
ls ext/decrease/210_Novel_Anticancer_combinations
