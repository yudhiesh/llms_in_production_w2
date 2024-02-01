FROM python:3.9-slim-bullseye

# Set working directory
ENV APP_HOME /app
ENV PYTHONPATH $APP_HOME
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y git gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies and install them
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Create a non-root user (if you decide to add this step)

# Copy application code
COPY src ./src
COPY .streamlit ./.streamlit

# Expose port and define command
EXPOSE 8080
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port", "8080"]
