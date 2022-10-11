FROM python:3.9.4-slim-buster

COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY ./src /app/

WORKDIR /app
CMD ["python", "app.py"]