from pydantic import BaseModel
from threedframe.models import ModelData


class GenerateRequest(BaseModel):
    model_data: ModelData
    vertex: int
