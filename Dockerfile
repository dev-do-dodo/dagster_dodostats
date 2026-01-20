FROM python:3.11

COPY . /

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /upload_dodostats/

EXPOSE 80
