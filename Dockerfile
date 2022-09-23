FROM python:3.10.7-alpine3.16

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "setup.py"]



