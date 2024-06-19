# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the Docker container
WORKDIR /app

# Install necessary build tools and dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the local code to the container's working directory.
COPY . /app

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to specify where the Flask application is
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]