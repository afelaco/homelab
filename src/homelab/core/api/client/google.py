# from time import sleep
# from typing import Any
#
# from google.oauth2 import service_account
#
# from homelab import SETTINGS
# from homelab.core import get_logger
# from homelab.core.api.client import ApiClient
# from homelab.core.endpoint import Endpoint
#
# logger = get_logger(name=__name__)
#
#
# class GoogleApiClient(ApiClient):
#     def __init__(self) -> None:
#         super().__init__(base_url="https://www.googleapis.com/drive/v3")
#
#     def get_auth_headers(self) -> dict[str, str]:
#         if not self.token:
#             self.get_token()
#         return {"Authorization": f"Bearer {self.token}"}
#
#     def get_token(self) -> None:
#         scopes = ["https://www.googleapis.com/auth/drive.readonly"]
#         return service_account.Credentials.from_service_account_info(
#             SETTINGS.GOOGLE_API_KEY,
#             scopes=scopes,
#         ).token
#
#     def get_url(self, endpoint: Endpoint) -> str:
#         return f"{self.base_url}/{endpoint.url}"
#
#     def get(
#         self,
#         endpoint: Endpoint,
#         params: dict[str, str] | None = None,
#     ) -> list[dict[str, Any]]:
#         url: str | None = self.get_url(endpoint=endpoint)
#         data: list[dict[str, Any]] = []
#
#         if params is None:
#             params = {}
#
#         while url:
#             response = self.session.get(
#                 url=url,
#                 params=params,
#             )
#             response.raise_for_status()
#
#             page = endpoint.model.model_validate_json(response.content).model_dump()
#
#             # Google Drive API returns lists under the 'files' key
#             if page.get("files"):
#                 data.extend(page["files"])
#             else:
#                 data.extend([page])
#
#             logger.info("%s records read from %s", len(data), url)
#
#             # Handle Google Drive's token-based pagination
#             next_page_token = page.get("nextPageToken")
#             if next_page_token:
#                 params["pageToken"] = next_page_token
#             else:
#                 url = None
#
#             sleep(1)
#
#         return data
