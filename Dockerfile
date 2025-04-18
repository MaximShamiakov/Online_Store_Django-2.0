# Use a stable and lightweight Python 3.10 image.
FROM python:3.10-slim

# Install build tools and Python dependencies required for some packages.
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set /app as the working directory inside the container.
WORKDIR /app
# Copy requirements.txt to the container.
COPY requirements.txt .
# Upgrade pip and install Python dependencies.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to the container.
COPY . .

# Expose port
EXPOSE 8000

# Run Django development server on container startup.
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]

