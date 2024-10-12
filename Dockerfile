FROM python:3.10.5-slim
WORKDIR /workdir

RUN mkdir -p /{keyframes,db}
RUN mkdir /workdir/ckpt

RUN ln -sf /keyframes /workdir/keyframes
RUN ln -sf /db /workdir/db

COPY . .

RUN ./first_run.bash

EXPOSE 8502

CMD ["streamlit","run","dashboard.py"]
