import re
from datetime import timedelta
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.db.models import Sum
from django.utils import timezone

from .models import OrderItem, Product


def get_best_selling_products(days=30, limit=12):
    since = timezone.now() - timedelta(days=days)
    best_sellers = (
        OrderItem.objects.filter(order__created_at__gte=since)
        .values("product")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:limit]
    )
    product_ids = [item["product"] for item in best_sellers]
    return Product.objects.filter(id__in=product_ids, is_active=True)


def update_featured_products(days=30, limit=12):
    from django.db.models import Sum

    since = timezone.now() - timedelta(days=days)
    ranking = (
        OrderItem.objects.filter(order__created_at__gte=since)
        .values("product")
        .annotate(total_quantity=Sum("quantity"))
        .order_by("-total_quantity")[:limit]
    )

    Product.objects.update(is_featured=False, featured_rank=None)
    for rank, item in enumerate(ranking, start=1):
        Product.objects.filter(id=item["product"]).update(is_featured=True, featured_rank=rank)


def fetch_amazon_product_data(url):
    parsed = urlparse(url)
    if "amazon." not in parsed.netloc:
        raise ValueError("URL must be an Amazon product link")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find(id="productTitle")
    price = soup.find(id="priceblock_ourprice") or soup.find(id="priceblock_dealprice")
    image = soup.find(id="landingImage") or soup.select_one("img#imgTagWrapperId img")
    description_tag = soup.find(id="feature-bullets")

    extracted = {
        "title": title.get_text(strip=True) if title else "",
        "price": float(re.sub(r"[^0-9.,]", "", price.get_text())) if price else None,
        "description": description_tag.get_text(separator="\n", strip=True) if description_tag else "",
        "image_url": image["src"] if image and image.has_attr("src") else None,
        "source_url": url,
    }
    return extracted
