# Stage 1: Build Stage
FROM python:3.12.4 AS build

WORKDIR /usr/src/app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Runtime Stage
FROM python:3.12.4-slim

WORKDIR /usr/src/app

# Install runtime dependencies
RUN pip install --no-cache-dir flask confluent_kafka flask_sqlalchemy flask_migrate python-decouple

# Copy only the necessary files from the build stage
COPY --from=build /usr/src/app /usr/src/app

# Install SQLite3 for debugging purposes (if necessary)
# RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*

CMD ["python", "app.py"]




# FROM python:3.12.4

# WORKDIR /usr/src/app

# COPY requirements.txt ./

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # # Install SQLite3
# # RUN apt-get update && apt-get install -y sqlite3

# COPY . .

# CMD ["python", "app.py"]


