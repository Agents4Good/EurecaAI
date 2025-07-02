FROM python:3.11-slim

WORKDIR /EurecaAI

RUN apt update && \
    apt install -y git vim && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Comando padrão para rodar a aplicação
CMD ["./venv/bin/python", "-m", "flask_app.app"]
