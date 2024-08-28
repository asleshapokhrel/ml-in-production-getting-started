FROM python:3.12-slim

# set working dir
WORKDIR /app

# copy requirement file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# expose port outside the container
EXPOSE 8000

# commands to run the application
CMD ["uvicorn", "hello_docker:app", "--host", "0.0.0.0", "--port", "8000"]
