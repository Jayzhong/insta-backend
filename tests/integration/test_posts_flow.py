import pytest
from httpx import ASGITransport, AsyncClient

from main import app

# We need a way to ensure a clean state or unique data for each run.
# For now, using unique usernames/emails is sufficient for a live integration test against a dev DB.

@pytest.mark.asyncio
async def test_posts_lifecycle_flow():
    """
    Integration test verifying the full lifecycle of a post:
    1. Register a new user
    2. Login to get token
    3. Create a post (upload image)
    4. Get the post by ID
    5. List posts by user
    """
    # Setup unique user data
    unique_id = "integration_test_user_" + str(id(app)) # Simple unique suffix
    username = f"user_{unique_id}"
    email = f"user_{unique_id}@example.com"
    password = "StrongPassword123!"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Register
        reg_response = await ac.post(
            "/api/v1/users/register",
            json={"username": username, "email": email, "password": password},
        )
        assert reg_response.status_code == 201
        user_id = reg_response.json()["id"]

        # 2. Login
        login_response = await ac.post(
            "/api/v1/users/login",
            json={"email": email, "password": password},
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Create Post
        # We simulate a file upload
        file_content = b"fake image content"
        files = {"image": ("test_image.jpg", file_content, "image/jpeg")}
        data = {"caption": "My first integration test post!"}

        create_response = await ac.post(
            "/api/v1/posts/",
            headers=headers,
            data=data,
            files=files,
        )
        assert create_response.status_code == 201, create_response.text
        post_data = create_response.json()
        post_id = post_data["id"]
        assert post_data["caption"] == "My first integration test post!"
        assert post_data["user_id"] == user_id
        assert post_data["image_url"].endswith(".jpg")

        # 4. Get Post by ID
        get_response = await ac.get(f"/api/v1/posts/{post_id}", headers=headers)
        assert get_response.status_code == 200
        fetched_post = get_response.json()
        assert fetched_post["id"] == post_id
        assert fetched_post["caption"] == "My first integration test post!"

        # 5. List Posts by User
        list_response = await ac.get(f"/api/v1/posts/user/{user_id}", headers=headers)
        assert list_response.status_code == 200
        posts_list = list_response.json()
        assert isinstance(posts_list, list)
        assert len(posts_list) >= 1
        # Check that our post is in the list
        assert any(p["id"] == post_id for p in posts_list)
