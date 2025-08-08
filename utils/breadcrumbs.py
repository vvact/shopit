from django.conf import settings


def build_breadcrumbs(category, product_slug=None, product_name=None):
    """
    Build frontend breadcrumbs from a category hierarchy and optionally a product.
    """
    breadcrumbs = []
    current = category

    while current:
        breadcrumbs.insert(0, {
            "label": current.name,
            "slug": current.slug,
        })
        current = current.parent

    full_path = ""
    for crumb in breadcrumbs:
        full_path += "/" + crumb["slug"]
        crumb["path"] = full_path
        del crumb["slug"]

    if product_slug:
        full_path += "/" + product_slug
        breadcrumbs.append({
            "label": product_name or product_slug.replace("-", " ").title(),
            "path": full_path
        })

    return breadcrumbs


def build_breadcrumb_schema(breadcrumbs, request=None):
    """
    Build schema.org BreadcrumbList for structured data (SEO).
    """
    base_url = (
        request.build_absolute_uri("/").rstrip("/") if request
        else getattr(settings, "SITE_URL", "http://localhost:8000").rstrip("/")
    )

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": crumb["label"],
                "item": f"{base_url}{crumb['path']}"
            }
            for idx, crumb in enumerate(breadcrumbs)
        ]
    }
