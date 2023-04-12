# Dockerfile

# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

COPY ./db/init.sql /docker-entrypoint-initdb.d/

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the entry point of the container
ENTRYPOINT ["python3", "entrypoint.py"]