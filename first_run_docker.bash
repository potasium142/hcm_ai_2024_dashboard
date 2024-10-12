#!/bin/bash

echo "Setup directory"

ln -sf /db /workdir/db
ln -sf /keyframes /workdir/keyframes

echo "Install debian packages"
apt update 
apt -y install wget git

echo "Install pip packages"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt --progress-bar on

echo "Download LongCLIP"
git submodule update --init --recursive

wget -q "https://huggingface.co/BeichenZhang/LongCLIP-L/resolve/main/longclip-L.pt" -P "./ckpt"

echo "Install nltk"
echo "import nltk; nltk.download('punkt_tab')" | python
