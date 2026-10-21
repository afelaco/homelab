from pandera.polars import DataFrameModel


class Model(DataFrameModel):
    class Config:
        strict = True
