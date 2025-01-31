# Use the Go base image
FROM golang:alpine

# Set environment variables to speed up builds
ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Set working directory
WORKDIR /app

# Copy only the go.mod and go.sum files for dependency caching
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download
RUN apk add --no-cache curl


# Copy the rest of the application
COPY . .

# Build the application
RUN go build -o service2 main.go

# Expose the port the service will listen on
EXPOSE 8199

# Run the service
CMD ["./service2"]
