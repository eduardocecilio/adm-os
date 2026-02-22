from database import engine, Base
from models.user import User

print("Forçando a criação manual das tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Sucesso! Tabelas ciradas.")
