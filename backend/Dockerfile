# Use an official Python runtime as a parent image
FROM python:3.10.13-alpine3.18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update pip and install gettext
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y gettext

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

EXPOSE 8000