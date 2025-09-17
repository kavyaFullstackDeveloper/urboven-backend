from django.core.management.base import BaseCommand
from properties.models import Property
from pathlib import Path
from decimal import Decimal, InvalidOperation
import json, re

def to_int(value, default=0):
    if value is None:
        return default
    if isinstance(value, int):
        return value
    # extract first number in strings like "2 BHK"
    m = re.search(r"\d+", str(value))
    return int(m.group()) if m else default

def to_decimal(value, default="0"):
    if value is None or value == "":
        return Decimal(default)
    try:
        # strip non-numeric except dot
        s = re.sub(r"[^0-9.]", "", str(value))
        return Decimal(s or default)
    except (InvalidOperation, TypeError):
        return Decimal(default)

class Command(BaseCommand):
    help = "Seed Property data from a JSON file (frontend shape)"

    def add_arguments(self, parser):
        parser.add_argument("--file", default="properties/seed/properties.json")

    def handle(self, *args, **opts):
        path = Path(opts["file"])
        if not path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        data = json.loads(path.read_text(encoding="utf-8"))
        objs = []
        for item in data:
            title = item.get("title") or "Property"
            location = item.get("location") or ""
            price = to_decimal(item.get("price"))
            bedrooms = to_int(item.get("bhk") or item.get("bedrooms"))
            bathrooms = to_int(item.get("bathrooms"))
            desc_parts = [
                item.get("description") or "",
                f"Avg price: {item.get('avg_price')}" if item.get("avg_price") else "",
            ]
            description = " ".join(p for p in desc_parts if p).strip() or "Seeded record"
            objs.append(Property(
                title=title,
                description=description,
                price=price,
                location=location,
                image="",  # set later or map a default
                bedrooms=bedrooms,
                bathrooms=bathrooms,
            ))

        Property.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(objs)} properties"))
