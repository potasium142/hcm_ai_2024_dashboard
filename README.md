# hcm_ai_2024
Chu?a test tren Windows

## Dataset data
1. [Set 1](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-keyframe-extract-1-kf) 
2. [Set 2](https://www.kaggle.com/datasets/huynhmy1/hcm-ai-keyframe-extract-2-kf)
3. [Set 3](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-keyframe-extract-l25-30)
3. [DB](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-db)

## Instruction
1. Extract all keyframes into **./keyframes**
2. Extract **DB** into **./db**

> [!IMPORTANT]  
> 3 CLIP models are about 15gb in size
> 
> For some reason, the progress bar for OpenCLIP downloading process no longer showup

### Local
1. Create an python 3.10.5 environment
2. Run **first_run.bash** (first_run.ps1 in powershell on Windows)
> [!WARNING]  
> DONT RUN ON WINDOWS, use docker instead

### Docker
#### Without Ollama / Non-local Ollama
1. Build docker image
```bash
docker build . --tag hcmai_c2024:dashboard
```
2. Run docker image
```bash
docker run --name hcm_ai_dashboard -p 8502:8502 -v ./keyframes:/keyframes -v ./db:/db hcmai_c2024:dashboard
```

> [!CAUTION]
> Ollama no workie rn, try run it seperately
#### With Ollama run locally
##### GPU
```bash
docker compose -f docker-compose-ollama-gpu.yaml up -d
```

##### CPU
```bash
docker compose  up -d
```

###### TODO
> Add extract process
