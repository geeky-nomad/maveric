from pydantic import BaseModel


class PartnerChatbotProfileResponse(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class WelcomeRequestSchema(BaseModel):
    user_id: int = None


class CategorySchema(BaseModel):
    user_id: int = None
    selected_category: str


class SubCategorySchema(CategorySchema):
    selected_sub_category: str


class ChitChatSchema(BaseModel):
    query: str
