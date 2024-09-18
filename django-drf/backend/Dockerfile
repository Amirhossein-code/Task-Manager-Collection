FROM python:3.12-alpine  

# Prevent Python from writing .pyc files to disc  
ENV PYTHONDONTWRITEBYTECODE 1  
# Set the buffering policy for stdout and stderr  
ENV PYTHONUNBUFFERED 1  

# Set the working directory in the container  
WORKDIR /app  

# Copy requirements file and install dependencies  
COPY requirements.txt .  
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt  

# Copy the entire application into the container  
COPY . .  

# Expose the port that the application runs on  
EXPOSE 8000  

# Set the entrypoint to the entrypoint script  
ENTRYPOINT ["sh", "/app/entrypoint.sh"]