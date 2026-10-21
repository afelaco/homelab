from pydantic import BaseModel, model_serializer


class QuerySummary(BaseModel):
    num_reviews: int
    review_score: int
    review_score_desc: str
    total_positive: int
    total_negative: int
    total_reviews: int


class SteamStoreAppReviewsApiResponseModel(BaseModel):
    query_summary: QuerySummary | None = None

    @model_serializer
    def serialize(self) -> QuerySummary | None:
        return self.query_summary
