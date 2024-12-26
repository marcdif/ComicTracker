FROM python:3.12-slim

WORKDIR /usr/src/app

COPY *.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py", "web_interface"]
