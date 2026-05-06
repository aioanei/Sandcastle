FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our Flask Python application
COPY app.py .

EXPOSE 80

CMD ["python", "app.py"]
