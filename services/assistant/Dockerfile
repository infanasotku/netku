FROM python:3.11

ADD . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app/manage.py"]
