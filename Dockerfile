# Base image for Python environment
FROM python:3.9-slim

# Create a directory for the application code
WORKDIR /app

# Install OpenJDK 17 and dependencies
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify Java
RUN java --version

# Copy requirements.txt
COPY requirements.txt .

# Set environment variables for Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install Python dependencies
RUN pip install -r requirements.txt

RUN pip show sqlalchemy

# Copy your application code
COPY . .

# Expose Python application port (modify if needed)
EXPOSE 8080

# Entrypoint command
CMD [ "python", "main.py" ]