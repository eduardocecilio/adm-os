# Usa uma imagem Python leve e oficial
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements primeiro (para aproveitar cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Comando para iniciar o servidor (liberando acesso externo com 0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]