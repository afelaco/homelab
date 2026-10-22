from pydantic import BaseModel


class OracleTagsScryfallResponseModel(BaseModel):
    compressed_size: int
    description: str
    id: str
    jsonl_download_uri: str
    name: str
    object: str
    type: str
    updated_at: str
    uri: str
