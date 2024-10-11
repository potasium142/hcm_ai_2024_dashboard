#TEST? NUN HUH

# Install pip packages
Write-Host "Install pip packages"
pip install -r requirements.txt --progress-bar on 
pip install torch torchvision torchaudio

# Download LongCLIP
Write-Host "Download LongCLIP"
Invoke-WebRequest -Uri "https://huggingface.co/BeichenZhang/LongCLIP-L/resolve/main/longclip-L.pt" -OutFile "./ckpt/longclip-L.pt"
git submodule update --init --recursive

# Install nltk
Write-Host "Install nltk"
python -c "import nltk; nltk.download('punkt_tab')"
