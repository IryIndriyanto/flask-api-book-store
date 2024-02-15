FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]