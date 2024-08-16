# Use an official Python runtime as a parent image
FROM python:3.12-alpine3.20

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first, so we can cache dependencies separately
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt &&\
    pip install python-multipart

# Copy the rest of the application code to the working directory
COPY . .

# Set the environment variables for Alembic
ENV PYTHONPATH=/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
