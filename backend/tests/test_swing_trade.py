import pytest
from fastapi.testclient import TestClient
from main import app
from services.swing_trade_service import calcular_swing_trade, DadosOperacao
from database import SessionLocal, Base, engine
from models.user import User
from auth_utils import get_password_hash, create_access_token

client = TestClient(app)

# --- Fixtures ---

def _get_or_create_test_token() -> str:
    """Cria um usuário de teste no banco e retorna um JWT válido."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "test@admosteste.com").first()
        if not user:
            user = User(
                email="test@admosteste.com",
                hashed_password=get_password_hash("senhateste123"),
                is_active=True,
            )
            db.add(user)
            db.commit()
        return create_access_token(data={"sub": "test@admosteste.com"})
    finally:
        db.close()


# --- Unit Tests ---

def test_calcular_swing_trade_lucro():
    """Testa o cálculo com lucro e imposto."""
    dados = DadosOperacao(
        preco_compra=10.00,
        preco_venda=12.00,
        quantidade=100,
        taxa_corretagem=5.00
    )
    resultado = calcular_swing_trade(dados)
    resumo = resultado["resumo"]

    assert resumo["lucro_bruto"] == 200.00
    # Custos: (5.00 * 2) + ((1000 + 1200) * 0.000345) = 10 + 0.759 = 10.759
    assert resumo["custos_totais"] == 10.759
    # IR: (200 - 10.759) * 0.15 = 28.38615 -> rounds to 28.3861
    assert resumo["imposto_renda"] == 28.3861
    # Lucro Líquido: 189.241 - 28.38615 = 160.85485 -> 160.85
    assert resumo["lucro_liquido"] == 160.85


def test_calcular_swing_trade_prejuizo():
    """Testa o cálculo com prejuízo (sem imposto)."""
    dados = DadosOperacao(
        preco_compra=12.00,
        preco_venda=10.00,
        quantidade=100,
        taxa_corretagem=5.00
    )
    resultado = calcular_swing_trade(dados)
    resumo = resultado["resumo"]

    assert resumo["lucro_bruto"] == -200.00
    assert resumo["imposto_renda"] == 0.0
    assert resumo["lucro_liquido"] < -200.00


def test_calcular_swing_trade_validacao_preco_negativo():
    """Testa que preço negativo é rejeitado pela validação Pydantic."""
    with pytest.raises(Exception):
        DadosOperacao(preco_compra=-1.0, preco_venda=12.0, quantidade=100)


def test_calcular_swing_trade_validacao_quantidade_zero():
    """Testa que quantidade zero é rejeitada pela validação Pydantic."""
    with pytest.raises(Exception):
        DadosOperacao(preco_compra=10.0, preco_venda=12.0, quantidade=0)


# --- Integration Tests ---

def test_endpoint_sem_token():
    """Tenta acessar rota protegida sem token — espera 401."""
    response = client.post("/investimentos/swing-trade/calcular", json={
        "preco_compra": 10.0,
        "preco_venda": 12.0,
        "quantidade": 100
    })
    assert response.status_code == 401


def test_endpoint_com_token_invalido():
    """Token JWT inválido deve retornar 401."""
    response = client.post(
        "/investimentos/swing-trade/calcular",
        json={"preco_compra": 10.0, "preco_venda": 12.0, "quantidade": 100},
        headers={"Authorization": "Bearer token-invalido-qualquer"},
    )
    assert response.status_code == 401


def test_endpoint_sucesso():
    """Token JWT válido deve retornar 200 com o resultado correto."""
    token = _get_or_create_test_token()
    response = client.post(
        "/investimentos/swing-trade/calcular",
        json={
            "preco_compra": 10.0,
            "preco_venda": 12.0,
            "quantidade": 100,
            "taxa_corretagem": 5.00,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    dados = response.json()
    assert "resumo" in dados
    assert dados["resumo"]["lucro_bruto"] == 200.00
