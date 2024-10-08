# Use a base image with Go pre-installed
FROM golang:alpine

# Set working directory
WORKDIR /app

# Install necessary utilities (ps, uptime)
RUN apk update && apk add --no-cache procps

# Copy the Go code into the container
COPY . .

# Build the application
RUN go build -o service2 main.go

# Expose the port the service will listen on
EXPOSE 8080

# Run the service
CMD ["./service2"]
