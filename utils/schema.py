# utils/schema.py

from django.conf import settings

def build_product_schema(product, request=None):
    base_url = request.build_absolute_uri("/")[:-1] if request else getattr(settings, "SITE_URL", "http://localhost:8000")
    
    image_urls = []
    if hasattr(product, 'images') and product.images.exists():
        image_urls = [base_url + img.image.url for img in product.images.all()]

    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "image": image_urls,
        "description": (product.description or "")[:300],
        "sku": product.slug,
        "brand": {
            "@type": "Brand",
            "name": "YourBrandName"  # Replace with actual brand if available
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "KES",
            "price": str(product.get_final_price()),  # ✅ Fixed
            "availability": "https://schema.org/InStock" if product.in_stock else "https://schema.org/OutOfStock",
            "url": f"{base_url}/products/{product.slug}"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": getattr(product, 'average_rating', 0),
            "reviewCount": getattr(product, 'review_count', 0)
        }
    }
