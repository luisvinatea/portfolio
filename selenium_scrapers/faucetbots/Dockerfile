# Use the official Python image as the base image
FROM python:3.12-slim

# Set environment variables to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y wget curl git unzip && \
    apt-get install -y firefox-esr && \
    apt-get install -y xvfb && \
    apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 && \
    apt-get clean

# Install geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
    && rm /tmp/geckodriver.tar.gz

# Create and set the working directory
WORKDIR /app

# Copy your application code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set the display to be used by Xvfb
ENV DISPLAY=:99

# Run Xvfb in the background and start your Python script
CMD ["sh", "-c", "Xvfb :99 -ac & python selenium_freebitco_in.py"]
