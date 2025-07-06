FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use Gunicorn as the entrypoint for production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "application:app"]
