# Use the Go base image
FROM golang:alpine

# Set working directory
WORKDIR /app

# Ensure the working directory is writable
RUN chmod -R 777 /app

# Copy the Go code into the container
COPY . .

# Build the application
RUN go build -o service2 main.go

# Expose the port the service will listen on
EXPOSE 8199

# Run the service
CMD ["./service2"]
