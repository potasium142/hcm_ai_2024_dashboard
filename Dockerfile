FROM python:3.10.5-slim
WORKDIR /workdir


VOLUME [ "/db","/keyframes" ]

COPY . .

RUN ./first_run_docker.bash
RUN ./first_run.bash

EXPOSE 8502

CMD ["streamlit","run","dashboard.py"]
