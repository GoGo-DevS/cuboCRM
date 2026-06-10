def branding(request):
    """Variables de marca disponibles en todos los templates."""
    return {
        "BRAND_NAME": "Creative Growth CRM",
        "BRAND_SHORT": "cub.",
        "BRAND_TAGLINE": "Creative Operations System",
    }
