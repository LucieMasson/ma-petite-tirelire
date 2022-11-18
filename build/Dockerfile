FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /tmp/*

COPY ./app/requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app .

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

#ENTRYPOINT ["/app/kubernetes/entrypoint.sh"]
CMD ["python", "controller/manage.py", "runserver", "0.0.0.0:8000"]
