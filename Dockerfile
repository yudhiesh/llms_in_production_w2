FROM python:3.9-slim-bullseye

# Set working directory
ENV APP_HOME /app
ENV PYTHONPATH $APP_HOME
WORKDIR $APP_HOME

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y git gcc \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy application code
COPY src ./src
COPY .streamlit ./.streamlit

# Expose port and define command
EXPOSE 8080
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port", "8080"]
