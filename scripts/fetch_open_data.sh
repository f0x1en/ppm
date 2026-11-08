#!/bin/sh
# Download open datasets used by the notebooks into ext/ (not tracked by git).
# Malani et al., Cancer Discov 2022; Zenodo 10.5281/zenodo.7370747; CC BY 4.0.
set -e
mkdir -p ext/malani2022
cd ext/malani2022
[ -f data.zip ] || curl -fL -o data.zip "https://zenodo.org/api/records/7370747/files/Functional_Precision_Medicine_Tumor_Board_AML.zip/content"
echo "expected size 38810683 bytes, got $(wc -c < data.zip)"
unzip -oq data.zip
ls -R | head -40
