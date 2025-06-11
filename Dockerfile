FROM python:3.11-slim

WORKDIR /EurecaAI

COPY . .

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["./venv/bin/python", "-m", "flask_app.app"]
