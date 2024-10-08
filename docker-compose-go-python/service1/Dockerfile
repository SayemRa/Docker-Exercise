# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install necessary utilities (ps, uptime)
RUN apt-get update && apt-get install -y procps

# Install Flask and requests
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8199 for external access
EXPOSE 8199

# Run the Flask app
CMD ["python", "app.py"]
