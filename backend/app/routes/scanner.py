from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import httpx
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["scanner"])


# ==================== SCHEMAS ====================
class ProductScanResponse(BaseModel):
    barcode: str
    product_name: Optional[str] = None
    product_name_de: Optional[str] = None
    product_name_en: Optional[str] = None
    brands: Optional[str] = None
    categories: Optional[str] = None
    ingredients_text: Optional[str] = None
    ingredients_text_de: Optional[str] = None
    ingredients_text_en: Optional[str] = None
    allergens: Optional[str] = None
    image_url: Optional[str] = None
    nutriscore_grade: Optional[str] = None
    nova_group: Optional[int] = None
    found: bool = False


# ==================== ENDPOINTS ====================
@router.get("/scanner/barcode/{barcode}", response_model=ProductScanResponse)
async def scan_barcode(barcode: str, current_user: User = Depends(get_current_user)):
    """
    Scannt einen Barcode und holt Produktdaten von Open Food Facts API.

    - **barcode**: EAN/UPC Barcode (8-13 digits)
    - **current_user**: Authentifizierter User

    Returns:
        ProductScanResponse mit Produktdetails
    """

    # Validate barcode format (basic check)
    if not barcode.isdigit() or len(barcode) < 8 or len(barcode) > 13:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid barcode format. Must be 8-13 digits.",
        )

    try:
        # Open Food Facts API Call
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"https://world.openfoodfacts.org/api/v2/product/{barcode}",
                headers={
                    "User-Agent": "KitchenHelper-AI/1.0 (https://github.com/MCCMDave/kitchenhelper-ai)"
                },
            )

            if response.status_code != 200:
                return ProductScanResponse(barcode=barcode, found=False)

            data = response.json()

            # Check if product was found
            if data.get("status") != 1:
                return ProductScanResponse(barcode=barcode, found=False)

            product = data.get("product", {})

            # Extract product data
            return ProductScanResponse(
                barcode=barcode,
                product_name=product.get("product_name"),
                product_name_de=product.get("product_name_de"),
                product_name_en=product.get("product_name_en"),
                brands=product.get("brands"),
                categories=product.get("categories"),
                ingredients_text=product.get("ingredients_text"),
                ingredients_text_de=product.get("ingredients_text_de"),
                ingredients_text_en=product.get("ingredients_text_en"),
                allergens=product.get("allergens"),
                image_url=product.get("image_url"),
                nutriscore_grade=product.get("nutriscore_grade"),
                nova_group=product.get("nova_group"),
                found=True,
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Open Food Facts API timeout. Please try again.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch product data: {str(e)}",
        )


@router.get("/scanner/search/{query}")
async def search_products(
    query: str,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
):
    """
    Sucht Produkte auf Open Food Facts by Name/Brand.

    - **query**: Suchbegriff (Name oder Marke)
    - **page**: Seitennummer (default: 1)
    - **page_size**: Ergebnisse pro Seite (default: 20)
    - **current_user**: Authentifizierter User

    Returns:
        List von Produkten
    """

    if len(query) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters.",
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://world.openfoodfacts.org/cgi/search.pl",
                params={
                    "search_terms": query,
                    "page": page,
                    "page_size": page_size,
                    "json": 1,
                },
                headers={
                    "User-Agent": "KitchenHelper-AI/1.0 (https://github.com/MCCMDave/kitchenhelper-ai)"
                },
            )

            if response.status_code != 200:
                return {"products": [], "count": 0, "page": page}

            data = response.json()
            products = []

            for product in data.get("products", []):
                products.append(
                    {
                        "barcode": product.get("code"),
                        "product_name": product.get("product_name"),
                        "brands": product.get("brands"),
                        "categories": product.get("categories"),
                        "image_url": product.get("image_url"),
                        "nutriscore_grade": product.get("nutriscore_grade"),
                    }
                )

            return {
                "products": products,
                "count": data.get("count", 0),
                "page": page,
                "page_size": page_size,
            }

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Open Food Facts API timeout. Please try again.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search products: {str(e)}",
        )
