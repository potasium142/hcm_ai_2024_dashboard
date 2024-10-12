FROM python:3.10.5-slim
WORKDIR /workdir

RUN mkdir -p /{keyframes,db}

RUN ln -sf /keyframes /workdir/keyframes
RUN ln -sf /db /workdir/db

COPY . .

RUN apt update

CMD ["ls","."]
