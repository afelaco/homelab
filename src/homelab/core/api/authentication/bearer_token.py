class BearerTokenAuthentication:
    def __init__(self, token: str):
        self.token = token

    def get_auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
