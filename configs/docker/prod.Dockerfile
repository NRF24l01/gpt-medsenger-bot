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

RUN set -e; apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers; \
    pip --no-cache-dir install uwsgi; \
 apk del .build-deps;

# Migrate the database
CMD flask db init || true
CMD flask db migrate && flask db upgrade

# Start the Flask application
# ENTRYPOINT ["/bin/sh", "/app/configs/docker/start-dev.sh"]
