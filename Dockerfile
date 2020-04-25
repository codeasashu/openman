FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
WORKDIR /app

COPY . .

RUN python setup.py install

CMD ["openman"]