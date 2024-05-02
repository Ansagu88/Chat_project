FROM python:3.10-alpine3.14

WORKDIR /Chat_project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install --upgrade pip
COPY requirements.txt /Chat_project/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /Chat_project/

COPY ./entrypoint.sh /Chat_project/entrypoint.sh

ENTRYPOINT ["/Chat_project/entrypoint.sh"]