import pytest
from httpx import ASGITransport, AsyncClient

from main import app

@pytest.mark.asyncio
async def test_follows_lifecycle_flow():
    """
    Integration test verifying the full lifecycle of follows:
    1. Register Users A and B
    2. User A follows User B
    3. Verify User A is in User B's followers
    4. Verify User B is in User A's following
    5. User A tries to follow User B again (fail)
    6. User A tries to follow User A (fail)
    7. User A unfollows User B
    8. Verify lists are updated
    """
    unique_suffix = str(id(app))
    
    # Helper to register and get token
    async def register_and_login(ac, name):
        username = f"{name}_{unique_suffix}"
        email = f"{name}_{unique_suffix}@example.com"
        password = "StrongPassword123!"
        
        # Register
        reg_res = await ac.post(
            "/api/v1/users/register",
            json={"username": username, "email": email, "password": password},
        )
        assert reg_res.status_code == 201
        user_id = reg_res.json()["id"]
        
        # Login
        login_res = await ac.post(
            "/api/v1/users/login",
            json={"email": email, "password": password},
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        return user_id, token, username

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register Users
        id_a, token_a, username_a = await register_and_login(ac, "user_a")
        id_b, token_b, username_b = await register_and_login(ac, "user_b")
        
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # 2. User A follows User B
        follow_res = await ac.post(f"/api/v1/users/{id_b}/follow", headers=headers_a)
        assert follow_res.status_code == 204

        # 3. Verify User A is in User B's followers
        # (Anyone can view followers, but let's use A's token)
        followers_res = await ac.get(f"/api/v1/users/{id_b}/followers", headers=headers_a)
        assert followers_res.status_code == 200
        followers_list = followers_res.json()
        assert len(followers_list) == 1
        assert followers_list[0]["id"] == id_a
        assert followers_list[0]["username"] == username_a

        # 4. Verify User B is in User A's following
        following_res = await ac.get(f"/api/v1/users/{id_a}/following", headers=headers_a)
        assert following_res.status_code == 200
        following_list = following_res.json()
        assert len(following_list) == 1
        assert following_list[0]["id"] == id_b

        # 5. User A tries to follow User B again (fail)
        dup_follow_res = await ac.post(f"/api/v1/users/{id_b}/follow", headers=headers_a)
        assert dup_follow_res.status_code == 400
        assert "already following" in dup_follow_res.json()["detail"].lower()

        # 6. User A tries to follow User A (fail)
        self_follow_res = await ac.post(f"/api/v1/users/{id_a}/follow", headers=headers_a)
        assert self_follow_res.status_code == 400
        assert "cannot follow yourself" in self_follow_res.json()["detail"].lower()

        # 7. User A unfollows User B
        unfollow_res = await ac.delete(f"/api/v1/users/{id_b}/follow", headers=headers_a)
        assert unfollow_res.status_code == 204

        # 8. Verify lists are updated (empty)
        followers_res_2 = await ac.get(f"/api/v1/users/{id_b}/followers", headers=headers_a)
        assert len(followers_res_2.json()) == 0
        
        following_res_2 = await ac.get(f"/api/v1/users/{id_a}/following", headers=headers_a)
        assert len(following_res_2.json()) == 0
        
        # 9. Unfollow again should fail
        dup_unfollow = await ac.delete(f"/api/v1/users/{id_b}/follow", headers=headers_a)
        assert dup_unfollow.status_code == 400
        assert "not following" in dup_unfollow.json()["detail"].lower()
