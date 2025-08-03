# products/management/commands/seed_categories.py

from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = "Seed categories with parent-child relationships for men's products"

    def handle(self, *args, **kwargs):
        data = {
            "Clothing": [
                "T-Shirts", "Shirts", "Trousers", "Jeans", "Shorts",
                "Suits & Blazers", "Jackets & Coats", "Hoodies & Sweatshirts", "Innerwear"
            ],
            "Footwear": [
                "Sneakers", "Formal Shoes", "Loafers", "Sandals & Slippers", "Boots"
            ],
            "Accessories": [
                "Belts", "Wallets", "Watches", "Sunglasses", "Hats & Caps",
                "Bags & Backpacks", "Ties & Cufflinks"
            ],
            "Grooming": [
                "Fragrances", "Beard Care", "Skin Care", "Hair Care"
            ],
            "Sportswear": [
                "Tracksuits", "Gym Shorts", "Sports Shoes", "Tank Tops"
            ],
        }

        for parent_name, children in data.items():
            parent, _ = Category.objects.get_or_create(name=parent_name, slug=parent_name.lower().replace(" ", "-"))
            for child_name in children:
                Category.objects.get_or_create(
                    name=child_name,
                    slug=child_name.lower().replace(" ", "-"),
                    defaults={"parent": parent}
                )

        self.stdout.write(self.style.SUCCESS("✅ Categories seeded successfully."))
