FROM python:3.5

WORKDIR /code
COPY ./code/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./code /code