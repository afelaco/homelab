import requests


class OAuth2Authentication:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        scope: str | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.scope = scope
        self.token = None

    def get_auth_headers(self) -> dict[str, str]:
        if not self.token:
            self.get_token()
        return {"Authorization": f"Bearer {self.token}"}

    def get_token(self) -> None:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
        }
        response = requests.post(
            url=self.token_url,
            data=data,
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]
