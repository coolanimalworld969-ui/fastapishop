from pydantic import BaseModel, Field, ConfigDict


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)

class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1)