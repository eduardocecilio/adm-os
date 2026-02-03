# Usa Python 3.9 para ser IDÊNTICO ao seu Mac e evitar erros de versão
FROM python:3.9-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements primeiro (para aproveitar cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]