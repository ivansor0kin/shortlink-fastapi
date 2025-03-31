from locust import HttpUser, task, between
import random

class ShortlinkUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://shortlink-fastapi.onrender.com"

    def on_start(self):
        # Регистрация и логин
        self.client.post("/register", json={"username": f"user{random.randint(1, 1000)}", "password": "test123"})
        response = self.client.post("/token", data={"username": "testuser", "password": "test123"})
        self.token = response.json()["access_token"]

    @task(3)
    def create_link(self):
        self.client.post("/links/", json={"original_url": f"https://example{random.randint(1, 1000)}.com"},
                         headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def get_link(self):
        self.client.get("/links/exmpl")

    @task(1)
    def search_link(self):
        self.client.get("/links/search?original_url=https://example.com")