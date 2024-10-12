FROM python:3.10.5-slim
WORKDIR /workdir

COPY . .

RUN ./first_run_docker.bash

EXPOSE 8502

CMD ["streamlit","run","dashboard.py"]
# CMD ["ls","/workdir/keyframes"]
