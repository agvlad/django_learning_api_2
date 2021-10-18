FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "net_api.wsgi"]
