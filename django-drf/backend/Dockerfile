# Use an official Python runtime as a parent image
FROM python:3.12-alpine3.20

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update package manager and install gettext
RUN apt-get update && apt-get install -y gettext


# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Copy the project code into the container
COPY . /app/

# Set the entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]

# Expose the port
EXPOSE 8000