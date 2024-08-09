# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Chromium and other dependencies
RUN apt-get update && \
    apt-get install -y chromium chromium-driver tzdata && \
    apt-get clean

# Set the timezone to Asia/Seoul
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# Set the working directory in the container
WORKDIR /app


# Copy the current directory contents into the container at /app
COPY . /app

# Install setuptools and pip
RUN pip install --upgrade pip setuptools

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run run.py when the container launches
CMD ["python", "run.py"]

