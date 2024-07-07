# Use the official Python 3.12 slim image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Update and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Copy requirements.txt to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Expose the port jupyter-lab will run on
EXPOSE 8888

ENV JUPYTER_TOKEN=mysecrettoken

# Run jupyter-lab without starting a browser
CMD ["sh", "-c", "jupyter-lab --no-browser --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token=${JUPYTER_TOKEN}"]
