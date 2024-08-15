# Use a base Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Migrate the database
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

# Expose the Flask application port
EXPOSE 8034

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8034"]
