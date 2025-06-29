FROM python:3.13.5

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY data_sentinel /app/data_sentinel
COPY data_sentinel/example_config.json /app/example_config.json

WORKDIR /app
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "data_sentinel.run", "example_config.json"]
