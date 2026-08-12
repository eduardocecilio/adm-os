import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt
from pydantic import ValidationError

import email_utils
from auth_utils import (
    ACCESS_TOKEN_TYPE,
    ALGORITHM,
    AUTH_VERSION_CLAIM,
    INVITE_TOKEN_TYPE,
    RESET_SECRET_KEY,
    RESET_TOKEN_TYPE,
    SECRET_KEY,
    TOKEN_TYPE_CLAIM,
    create_access_token,
    create_invite_token,
    create_reset_token,
    get_password_hash,
    verify_invite_token,
    verify_reset_token,
)
from dependencies import get_current_user
from database import Base, SessionLocal, engine
from main import app
from models.user import User
from models.workspace import Workspace, WorkspaceRole as ModelWorkspaceRole, WorkspaceUser
from routers.users import UserUpdate
from routers.exportar import safe_spreadsheet_text, sanitize_spreadsheet_rows
from routers import workspaces as workspaces_router
from schemas.workspace import WorkspaceInvite, WorkspaceRole


client = TestClient(app)


def test_tokens_have_distinct_enforced_types():
    access_token = create_access_token(
        {"sub": "user@example.com", TOKEN_TYPE_CLAIM: INVITE_TOKEN_TYPE},
        auth_version=3,
    )
    reset_token = create_reset_token("user@example.com", auth_version=3)
    invite_token = create_invite_token("user@example.com", 42, "MEMBER")

    access_payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    reset_payload = jwt.decode(reset_token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
    invite_payload = jwt.decode(invite_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert access_payload[TOKEN_TYPE_CLAIM] == ACCESS_TOKEN_TYPE
    assert access_payload[AUTH_VERSION_CLAIM] == 3
    assert reset_payload[TOKEN_TYPE_CLAIM] == RESET_TOKEN_TYPE
    assert reset_payload[AUTH_VERSION_CLAIM] == 3
    assert invite_payload[TOKEN_TYPE_CLAIM] == INVITE_TOKEN_TYPE
    assert verify_reset_token(reset_token) == {
        "email": "user@example.com",
        "auth_version": 3,
    }
    assert verify_invite_token(invite_token) == {
        "email": "user@example.com",
        "workspace_id": 42,
        "role": "MEMBER",
    }


def test_invite_token_cannot_be_used_as_bearer_token():
    invite_token = create_invite_token("user@example.com", 42, "MEMBER")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_current_user(token=invite_token, db=None))

    assert exc_info.value.status_code == 401


def test_token_verifiers_reject_wrong_or_missing_types():
    expires = datetime.utcnow() + timedelta(minutes=5)
    wrong_reset = jwt.encode(
        {
            "sub": "user@example.com",
            "exp": expires,
            TOKEN_TYPE_CLAIM: ACCESS_TOKEN_TYPE,
        },
        RESET_SECRET_KEY,
        algorithm=ALGORITHM,
    )
    untyped_invite = jwt.encode(
        {
            "sub": "user@example.com",
            "workspace_id": 42,
            "role": "MEMBER",
            "exp": expires,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    assert verify_reset_token(wrong_reset) is None
    assert verify_invite_token(untyped_invite) is None


def test_invites_reject_owner_guest_and_invalid_email():
    for role in (WorkspaceRole.OWNER, WorkspaceRole.GUEST):
        with pytest.raises(ValidationError):
            WorkspaceInvite(email="user@example.com", role=role)
        with pytest.raises(ValueError):
            create_invite_token("user@example.com", 42, role)

    with pytest.raises(ValidationError):
        WorkspaceInvite(email="not-an-email", role=WorkspaceRole.MEMBER)


def test_manually_signed_owner_invite_is_rejected():
    owner_invite = jwt.encode(
        {
            "sub": "user@example.com",
            "workspace_id": 42,
            "role": "OWNER",
            "exp": datetime.utcnow() + timedelta(minutes=5),
            TOKEN_TYPE_CLAIM: INVITE_TOKEN_TYPE,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    assert verify_invite_token(owner_invite) is None


def test_profile_password_requires_current_password_and_eight_characters():
    with pytest.raises(ValidationError):
        UserUpdate(password="12345678")

    with pytest.raises(ValidationError):
        UserUpdate(current_password="current-password", password="short")

    update = UserUpdate(
        current_password="current-password",
        password="12345678",
    )
    assert update.password == "12345678"


def test_spreadsheet_formula_prefixes_are_neutralized():
    assert safe_spreadsheet_text("=HYPERLINK(\"https://example.test\")") == "'=HYPERLINK(\"https://example.test\")"
    assert safe_spreadsheet_text("@SUM(1,1)") == "'@SUM(1,1)"
    assert safe_spreadsheet_text("  =1+1") == "'  =1+1"
    assert safe_spreadsheet_text("\t-2+3") == "'\t-2+3"
    assert safe_spreadsheet_text("Conta segura") == "Conta segura"

    assert sanitize_spreadsheet_rows([
        {"Indicador": "=CMD()", "Valor": "+1", "Seguro": 42}
    ]) == [
        {"Indicador": "'=CMD()", "Valor": "'+1", "Seguro": 42}
    ]


def test_public_registration_is_blocked_for_external_hosts():
    response = client.post(
        "/auth/register",
        headers={"host": "demo.example.test"},
        json={
            "email": f"external-{uuid4().hex}@example.com",
            "password": "password-segura",
            "workspace_name": "External",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"].startswith("Cadastro público desativado")


def test_local_registration_remains_available_for_the_demo():
    Base.metadata.create_all(bind=engine)
    unique = uuid4().hex
    email = f"local-{unique}@example.com"
    workspace_name = f"Local demo {unique}"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "password-segura",
            "workspace_name": workspace_name,
        },
    )

    assert response.status_code == 200
    access_payload = jwt.decode(
        response.json()["access_token"],
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
    assert access_payload[AUTH_VERSION_CLAIM] == 0

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        workspace = db.query(Workspace).filter(Workspace.name == workspace_name).first()
        if user:
            db.delete(user)
        if workspace:
            db.delete(workspace)
        db.commit()
    finally:
        db.close()


def test_password_reset_is_single_use_and_revokes_existing_access_tokens():
    Base.metadata.create_all(bind=engine)
    unique = uuid4().hex
    email = f"reset-{unique}@example.com"

    db = SessionLocal()
    user = User(
        email=email,
        hashed_password=get_password_hash("senha-antiga-segura"),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    reset_token = create_reset_token(email, auth_version=user.auth_version)
    access_token = create_access_token(
        {"sub": email},
        auth_version=user.auth_version,
    )

    try:
        first_reset = client.post(
            "/auth/reset-password",
            json={"token": reset_token, "new_password": "senha-nova-segura"},
        )
        second_reset = client.post(
            "/auth/reset-password",
            json={"token": reset_token, "new_password": "outra-senha-segura"},
        )
        old_session = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert first_reset.status_code == 200
        assert second_reset.status_code == 400
        assert second_reset.json()["detail"] == "Token inválido ou já utilizado"
        assert old_session.status_code == 401
    finally:
        db.expire_all()
        persisted_user = db.query(User).filter(User.email == email).first()
        if persisted_user:
            db.delete(persisted_user)
            db.commit()
        db.close()


def test_email_html_escapes_message_and_link(monkeypatch):
    captured = {}

    class Response:
        def raise_for_status(self):
            return None

    def fake_post(url, **kwargs):
        captured.update(kwargs)
        return Response()

    monkeypatch.setattr(email_utils.settings, "N8N_WEBHOOK_URL", "https://example.test/hook")
    monkeypatch.setattr(email_utils.settings, "N8N_WEBHOOK_TOKEN", "test-token")
    monkeypatch.setattr(email_utils.settings, "EMAIL_FROM", "sender@example.test")
    monkeypatch.setattr(email_utils.requests, "post", fake_post)

    asyncio.run(
        email_utils.send_email(
            subject="Test",
            email_to=["user@example.com"],
            body={
                "message": '<img src=x onerror="alert(1)">',
                "link": 'https://example.test/?q="><script>alert(1)</script>',
            },
        )
    )

    html = captured["json"]["html"]
    assert "<img" not in html
    assert "<script>" not in html
    assert "&lt;img" in html
    assert "&quot;&gt;&lt;script&gt;" in html


def test_invite_endpoint_is_rate_limited(monkeypatch):
    async def fake_send_email(**kwargs):
        return None

    monkeypatch.setattr(workspaces_router, "send_email", fake_send_email)

    Base.metadata.create_all(bind=engine)
    unique = uuid4().hex
    owner_email = f"owner-{unique}@example.com"
    invited_email = f"invited-{unique}@example.com"

    db = SessionLocal()
    owner = User(
        email=owner_email,
        hashed_password="not-used-by-this-test",
        is_active=True,
    )
    workspace = Workspace(name=f"Workspace {unique}")
    db.add_all([owner, workspace])
    db.commit()
    db.refresh(owner)
    db.refresh(workspace)
    link = WorkspaceUser(
        workspace_id=workspace.id,
        user_id=owner.id,
        role=ModelWorkspaceRole.OWNER,
    )
    db.add(link)
    db.commit()

    token = create_access_token({"sub": owner_email})
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"email": invited_email, "role": "MEMBER"}

    try:
        responses = [
            client.post(
                f"/workspaces/{workspace.uuid}/invite",
                json=payload,
                headers=headers,
            )
            for _ in range(6)
        ]

        assert [response.status_code for response in responses[:5]] == [200] * 5
        assert responses[5].status_code == 429
    finally:
        db.delete(link)
        db.delete(workspace)
        db.delete(owner)
        db.commit()
        db.close()
