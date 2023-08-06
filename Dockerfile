# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the current directory into the container's working directory
COPY . .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask application will be running on
EXPOSE 5000

# Start the Flask application when the container starts
CMD ["python", "main.py"]
