FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 9000

# Define environment variable
ENV STREAMLIT_SERVER_PORT=9000

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
