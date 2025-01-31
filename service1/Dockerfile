FROM python:3.8-slim
WORKDIR /app
RUN apt-get update && apt-get install -y procps
<<<<<<< HEAD
=======
RUN apt-get update && apt-get install -y curl

# Install Flask and requests
>>>>>>> ca42d59
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Expose port 8199 for external access
EXPOSE 8199

# Run the Flask app
CMD ["python", "app.py"]
