from base64 import b64encode


class BasicAuthentication:
    def __init__(self, username: str, password: str):
        self.username = username
        self.__password = password

    def get_auth_headers(self) -> dict[str, str]:
        bytestring = f"{self.username}:{self.__password}".encode()
        b64_userpass = b64encode(bytestring).decode("ascii")
        return {"Authorization": f"Basic {b64_userpass}"}
