FROM python:3.9

RUN useradd shredhub

RUN mkdir /home/shredhub
WORKDIR /home/shredhub

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt requirements.txt
# RUN python3 -m venv venv
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY app app
COPY migrations migrations
COPY logs logs
COPY .env shredhub.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP shredhub.py

RUN chown -R shredhub:shredhub ./
USER shredhub

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]


# docker build -t shredhub:latest . && docker image prune
# docker run --name shredhub -p 8000:5000 --rm shredhub:latest