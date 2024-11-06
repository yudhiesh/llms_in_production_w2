FROM python:3.10-slim-bullseye

# Set up ARGs to receive build-time values from docker-compose
ARG GUARDRAILS_TOKEN
ARG OPENAI_API_KEY

# Set environment variables from the build arguments
ENV APP_HOME /app
ENV PYTHONPATH $APP_HOME
ENV GUARDRAILS_TOKEN=${GUARDRAILS_TOKEN}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

WORKDIR $APP_HOME

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y build-essential git gcc \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Run Guardrails configuration
RUN guardrails configure --enable-metrics --enable-remote-inferencing --token $GUARDRAILS_TOKEN
RUN guardrails hub install hub://guardrails/valid_sql

# Copy application source files
COPY src ./src
COPY .streamlit ./.streamlit

# Expose the port for Streamlit
EXPOSE 8080

# Command to run the application
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port", "8080"]
