FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

COPY docker_entrypoint.sh .
RUN chmod +x docker_entrypoint.sh
ENTRYPOINT ["/app/docker_entrypoint.sh"]
