FROM python:3.11.2-slim-bullseye
WORKDIR /
COPY multi /multi
CMD ["python", "-m", "multi"]
