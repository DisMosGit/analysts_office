FROM python:3.9.1-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
COPY . ./

EXPOSE 8000
ENTRYPOINT ["python"]