FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install pika
CMD ["python", "publisher.py"]
