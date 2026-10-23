from homelab import SETTINGS
from homelab.core import get_logger

logger = get_logger(name=__name__)


class Database:
    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: str = "5432",
        database: str = "postgres",
    ) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def get_connection_string(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


DWH = Database(
    username=SETTINGS.POSTGRES_USER,
    password=SETTINGS.POSTGRES_PASSWORD,
)
