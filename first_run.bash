#!/bin/bash
echo "Install pip packages"

pip install -r requirements.txt --progress-bar on -q

echo "Download LongCLIP"
git submodule update --init --recursive

wget -q --show-progress "https://huggingface.co/BeichenZhang/LongCLIP-L/resolve/main/longclip-L.pt" -P "./ckpt"

echo "Install nltk"
echo "import nltk; nltk.download('punkt_tab')" | python