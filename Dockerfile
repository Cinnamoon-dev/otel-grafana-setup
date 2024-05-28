FROM python:3.12-slim

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python3", "main.py" ]