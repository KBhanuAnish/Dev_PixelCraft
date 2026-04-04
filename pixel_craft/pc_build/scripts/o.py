import os
import sys
import django

# 1. Point Python to your main project root (two folders up from /scripts/o.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# 2. Tell Django where your settings are
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixel_craft.settings') 

# 3. Boot up Django
django.setup()

# 4. 🔥 Use an ABSOLUTE import, not a relative one!
from pc_build.models import Components

# ================= Dataset =================
components_data = [
    # ================= CPU =================
    {
        "name": "Ryzen 5 5600X", "brand": "AMD", "category": "CPU",
        "specs": {"cores": 6, "threads": 12, "socket": "AM4"},
        "image_url": "http://127.0.0.1:8000/media/component_images/AMD_Ryzen_5_5600X.jpg",
        "price": 18000, "stock": 10
    },
    {
        "name": "Ryzen 7 5800X", "brand": "AMD", "category": "CPU",
        "specs": {"cores": 8, "threads": 16, "socket": "AM4"},
        "image_url": "http://127.0.0.1:8000/media/component_images/AMD_Ryzen_7_5800X.jpg",
        "price": 26000, "stock": 8
    },
    {
        "name": "Core i5-12400F", "brand": "Intel", "category": "CPU",
        "specs": {"cores": 6, "threads": 12, "socket": "LGA1700"},
        "image_url": "http://127.0.0.1:8000/media/component_images/Intel_Core_i5-12400F.jpg",
        "price": 17000, "stock": 12
    },
    {
        "name": "Core i7-12700K", "brand": "Intel", "category": "CPU",
        "specs": {"cores": 12, "threads": 20, "socket": "LGA1700"},
        "image_url": "http://127.0.0.1:8000/media/component_images/Intel_Core_i7-12700K.jpg",
        "price": 32000, "stock": 6
    },

    # ================= GPU =================
    {
        "name": "Radeon RX 6600", "brand": "AMD", "category": "GPU",
        "specs": {"vram": "8GB", "architecture": "RDNA 2"},
        "image_url": "http://127.0.0.1:8000/media/component_images/AMD_RX_6600.jpg",
        "price": 25000, "stock": 7
    },
    {
        "name": "Radeon RX 7900 XT", "brand": "AMD", "category": "GPU",
        "specs": {"vram": "20GB", "architecture": "RDNA 3"},
        "image_url": "http://127.0.0.1:8000/media/component_images/AMD_RX_7900_XT.jpg",
        "price": 85000, "stock": 3
    },
    {
        "name": "GeForce RTX 3060", "brand": "NVIDIA", "category": "GPU",
        "specs": {"vram": "12GB", "architecture": "Ampere"},
        "image_url": "http://127.0.0.1:8000/media/component_images/NVIDIA_RTX_3060.jpg",
        "price": 32000, "stock": 5
    },
    {
        "name": "GeForce RTX 4070", "brand": "NVIDIA", "category": "GPU",
        "specs": {"vram": "12GB", "architecture": "Ada Lovelace"},
        "image_url": "http://127.0.0.1:8000/media/component_images/NVIDIA_RTX_4070.jpg",
        "price": 60000, "stock": 4
    },

    # ================= RAM =================
    {
        "name": "Vengeance LPX 16GB", "brand": "Corsair", "category": "RAM",
        "specs": {"capacity": "16GB", "type": "DDR4", "speed": "3200MHz"},
        "image_url": "http://127.0.0.1:8000/media/component_images/Corsair_Vengeance_LPX_16GB.jpg",
        "price": 4000, "stock": 20
    },
    {
        "name": "Trident Z 32GB", "brand": "G.SKILL", "category": "RAM",
        "specs": {"capacity": "32GB", "type": "DDR4", "speed": "3600MHz"},
        "image_url": "http://127.0.0.1:8000/media/component_images/G.SKILL_Trident_Z_32GB.jpg",
        "price": 9000, "stock": 10
    },

    # ================= STORAGE =================
    {
        "name": "Samsung 970 EVO 1TB", "brand": "Samsung", "category": "Storage",
        "specs": {"type": "NVMe SSD", "capacity": "1TB"},
        "image_url": "http://127.0.0.1:8000/media/component_images/Samsung_970_EVO.jpg",
        "price": 7000, "stock": 15
    },
    {
        "name": "WD Blue 2TB HDD", "brand": "Western Digital", "category": "Storage",
        "specs": {"type": "HDD", "capacity": "2TB"},
        "image_url": "http://127.0.0.1:8000/media/component_images/WD_Blue_2TB.jpg",
        "price": 4500, "stock": 12
    },

    # ================= PSU =================
    {
        "name": "Corsair 650W PSU", "brand": "Corsair", "category": "PSU",
        "specs": {"efficiency": "80+ Bronze"},
        "image_url": "http://127.0.0.1:8000/media/component_images/Corsair_650W.jpg",
        "price": 5000, "stock": 9
    },

    # ================= CASE =================
    {
        "name": "NZXT H510", "brand": "NZXT", "category": "Case",
        "specs": {"type": "Mid Tower"},
        "image_url": "http://127.0.0.1:8000/media/component_images/NZXT_H510.jpg",
        "price": 6000, "stock": 6
    },

    # ================= MONITOR =================
    {
        "name": "LG UltraGear 24\"", "brand": "LG", "category": "Monitor",
        "specs": {"refresh_rate": "144Hz", "resolution": "1080p"},
        "image_url": "http://127.0.0.1:8000/media/component_images/LG_UltraGear.jpg",
        "price": 15000, "stock": 7
    }
]

print("🧹 Cleaning database...")
Components.objects.all().delete()

for data in components_data:
    Components.objects.create(
        name=data["name"],
        brand=data["brand"],
        category=data["category"],
        price=data["price"],
        stock=data["stock"],
        specs=str(data["specs"]),   # IMPORTANT
        image_url=data["image_url"]
    )

print("✅ ALL COMPONENTS INSERTED SUCCESSFULLY!")