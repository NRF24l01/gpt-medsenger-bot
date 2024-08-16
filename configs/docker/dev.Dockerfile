# Use a base Python image
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY ./ ./

# Migrate the database
RUN flask db init || true

# Start the Flask application
# ENTRYPOINT ["/bin/sh", "/app/configs/docker/start-dev.sh"]
