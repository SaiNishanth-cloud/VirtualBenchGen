# Base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the entry point command
CMD ["python", "main.py"]
