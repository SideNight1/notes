from locust import HttpUser, between, task


class NotesUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def list_notes(self):
        with self.client.get(
            "/",
            name="Список заметок",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")