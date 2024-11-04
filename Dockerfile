FROM python:3.10-slim-bullseye

ARG GUARDRAILS_TOKEN
ARG OPENAI_API_KEY

ENV APP_HOME /app
ENV PYTHONPATH $APP_HOME

WORKDIR $APP_HOME

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y git gcc \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src ./src
COPY .streamlit ./.streamlit

EXPOSE 8080
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port", "8080"]
