# Use an appropriate Python Alpine image
FROM python:3.10-alpine3.18

# Set working directory
WORKDIR /server

# Install any necessary system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port your app listens on
EXPOSE 5000

# Run your Flask app (no need for "flask run" with this setup)
CMD ["python", "server.py"]