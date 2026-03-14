import os

# Define variáveis obrigatórias antes de qualquer import do projeto
os.environ.setdefault("SECRET_KEY", "test-secret-key-nao-usar-em-producao-1234567890abcdef")
os.environ.setdefault("RESET_SECRET_KEY", "test-reset-key-nao-usar-em-producao-1234567890abcdef")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_adm_os.db")
