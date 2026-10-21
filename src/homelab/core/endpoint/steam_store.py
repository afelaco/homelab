from homeauto.core.api.response_model.steam_store.app_details import (
    SteamStoreAppDetailsApiResponseModel,
)
from homeauto.core.api.response_model.steam_store.app_reviews import (
    SteamStoreAppReviewsApiResponseModel,
)
from homeauto.core.endpoint import Endpoint

appdetails = Endpoint(
    url="api/appdetails",
    response_model=SteamStoreAppDetailsApiResponseModel,
)

appreviews = Endpoint(
    url="appreviews",
    response_model=SteamStoreAppReviewsApiResponseModel,
)
