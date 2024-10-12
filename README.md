# hcm_ai_2024
Chu?a test tren Windows

## Dataset data
1. [Set 1](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-keyframe-extract-1-kf) 
2. [Set 2](https://www.kaggle.com/datasets/huynhmy1/hcm-ai-keyframe-extract-2-kf)
3. [Set 3 (incoming)]()
3. [DB](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-db)
## ~Buoc' de^? chay.~ (DONT USE THIS)
1. first_run.ps1
2. tai? dataset ve^'
3. Extract set 1, set 2 vao' **keyframes**
4. Extract DB vao' **db**

Le^.nh chay. dashboard
```bash
streamlit run dashboard.py
```
## Docker
1. Extract all keyframes into **./keyframes**
2. Extract **DB** into ./db
### Without Ollama
1. Build docker image
```bash
docker build . --tag potasium:hcm_ai_dashboard
```
2. Run docker image
```bash
docker run --name hcm_ai_dashboard -p 8502:8502 -v ./keyframes:/keyframes -v ./db:/db potasium:hcm_ai_dashboard
```
