FROM python:3.9.10-slim-buster

# Set working directory within container
WORKDIR /app

# Copy repository to container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run app when the container starts
CMD ["python", "./main.py"]