FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/marcdif/ComicTracker"

WORKDIR /usr/src/app

COPY *.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py", "web_interface"]
