FROM python:3.11.2-slim-bullseye
WORKDIR /
RUN pip install --no-cache-dir --upgrade pip==23.0.1 \
 && pip install --no-cache-dir aiomultiprocess==0.9.0
COPY multi /multi
CMD ["python", "-m", "multi"]
