from app.core.config import settings

def test_login(client, db):
    # First create a user
    from app.services import user
    from app.schemas.user import UserCreate
    from app.models.user import RoleEnum
    
    user.create(db, obj_in=UserCreate(
        email="test@neofactory.com",
        password="password123",
        role=RoleEnum.ADMINISTRATOR
    ))
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "test@neofactory.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
