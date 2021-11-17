from locust import HttpUser, task, between


class TestUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()

    def login(self):
        response = self.client.get("/member/login/")
        csrftoken = response.cookies['csrftoken']
        self.client.post("/member/login/",
                         data={"email": "dls4585@naver.com", "password": "123"}, headers={"X-CSRFToken": csrftoken})

    def logout(self):
        self.client.get("/member/logout/")

    @task
    def task1(self):
        self.client.get("/")
