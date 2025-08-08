def build_breadcrumbs(category, product=None, product_slug=None, product_name=None):
    """
    Build a breadcrumb trail for the given category and optionally a product.

    Args:
        category (Category): The category object (must have .name, .slug, and .parent).
        product (Product, optional): The product object with .name and .slug.
        product_slug (str, optional): Use this if product object is not available.
        product_name (str, optional): Optional name override when using product_slug.

    Returns:
        list: List of dicts with 'label' and 'path' keys.
    """
    if not hasattr(category, 'name') or not hasattr(category, 'slug') or not hasattr(category, 'parent'):
        raise TypeError(f"Invalid category object passed to build_breadcrumbs: {category!r}")

    breadcrumbs = []
    current = category

    # Build category trail
    while current:
        breadcrumbs.insert(0, {
            "label": current.name,
            "slug": current.slug,
        })
        current = current.parent

    # Build paths
    full_path = ""
    for crumb in breadcrumbs:
        full_path += "/" + crumb["slug"]
        crumb["path"] = full_path
        del crumb["slug"]

    # Append product (if passed)
    if product and hasattr(product, 'name') and hasattr(product, 'slug'):
        breadcrumbs.append({
            "label": product.name,
            "path": f"{full_path}/{product.slug}"
        })
    elif product_slug:
        breadcrumbs.append({
            "label": product_name or product_slug.replace("-", " ").title(),
            "path": f"{full_path}/{product_slug}"
        })

    return breadcrumbs
