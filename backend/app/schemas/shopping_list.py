# Shopping List Schemas
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ShoppingListItem(BaseModel):
    """Single item in shopping list"""
    name: str
    amount: str
    category: Optional[str] = None
    checked: bool = False


class ShoppingListRequest(BaseModel):
    """Request to generate shopping list"""
    recipe_ids: List[int] = Field(default=[], description="Recipe IDs to include")
    favorite_ids: List[int] = Field(default=[], description="Favorite IDs to include")
    scale_factor: float = Field(default=1.0, ge=0.5, le=10.0, description="Scale ingredients by factor")


class ShoppingListResponse(BaseModel):
    """Shopping list response"""
    items: List[ShoppingListItem]
    total_items: int
    recipes_included: List[str]
    created_at: datetime


class ShareLinkResponse(BaseModel):
    """Response with share link"""
    share_id: str
    share_url: str
    expires_at: datetime
    recipe_name: str
