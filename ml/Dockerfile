# Use an official Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "ml_api:app", "--host", "0.0.0.0", "--port", "8000"]
