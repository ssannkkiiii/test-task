FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install dependencies
RUN apt-get update && apt-get install -y postgresql-client libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Wait for database and start server
CMD sh -c "sleep 10 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
