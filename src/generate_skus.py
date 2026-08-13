import random
import pandas as pd

SKU_PATTERNS = {
    "Corvel" : 
    {"Brake Pad" : "CLBP",
    "Brake Disc" : "CLBD",
    "Brake Shoe" : "CLBK",
    "Engine Oil Filter": "CLEOF",
    "Engine Air Filter": "CLEAF",
    "Engine Fuel Filter": "CLEFF",
    "Engine Kabin Filter": "CLEKF",
    "Control Arm" : "CLCA",
    "Stabilizer Link" : "CLSL",
    "Tie Rod" : "CLTR"
    },

    "Axiom" :{
    "Brake Pad" : "AXBP",
    "Brake Disc" : "AXBD",
    "Brake Shoe" : "AXBK"
    },
    
    "Voltrix" : {
        "Brake Pad" : "VXBP",
        "Brake Disc" : "VXBD",
        "Engine Air Filter" : "VXAF",
        "Engine Oil Filter" : "VXOF",
        "Engine Fuel Filter" : "VXFF",
        "Steering Kit" : "VXSK",
    }
}


def generate_part():
    number = random.randint(1000, 9999)
    all_categories = []
    for brand_dict in SKU_PATTERNS.values():
        all_categories.extend(brand_dict.keys())
    category = random.choice(all_categories)

    eligible_brands = []
    for brand_name, brand_dict in SKU_PATTERNS.items():
        if category in brand_dict:
            eligible_brands.append(brand_name)

    brand = random.choice(eligible_brands)

    return number, category, brand

def generate_sku(number,category,brand):
    prefix = SKU_PATTERNS[brand][category]
    return prefix + str(number)


WEIGHT_RANGES = {
    "Brake Pad": (1.0, 4.5),
    "Brake Disc": (4.0, 15.0),
    "Brake Shoe": (1.0, 4.5),  
    "Engine Oil Filter": (0.3, 0.5),
    "Engine Air Filter": (0.3, 0.5),
    "Engine Fuel Filter": (0.3, 0.5),
    "Engine Kabin Filter": (0.3, 0.5),  
    "Control Arm": (0.5, 6.0),
    "Stabilizer Link": (0.5, 1.5),      
    "Tie Rod": (0.5, 1.5),              
    "Steering Kit": (0.5, 3.0),
}

def generate_weight(category):
    min_weight, max_weight = WEIGHT_RANGES[category]
    weight = random.uniform(min_weight, max_weight)
    return(round(weight,2))

DIMENSION_RANGES = {
    "Brake Disc": {"length": (27, 40), "width": (27, 40), "height": (4, 6)},
    "Brake Pad": {"length": (15, 25), "width": (10, 15), "height": (5, 8)},
    "Brake Shoe": {"length": (15, 25), "width": (10, 15), "height": (5, 8)},
    "Engine Oil Filter": {"length": (8, 8), "width": (8, 8), "height": (10, 11)},
    "Engine Air Filter": {"length": (20, 30), "width": (15, 20), "height": (5, 8)},
    "Engine Fuel Filter": {"length": (8, 10), "width": (8, 10), "height": (10, 14)},
    "Engine Kabin Filter": {"length": (20, 25), "width": (15, 20), "height": (3, 5)},
    "Control Arm": {"length": (40, 60), "width": (10, 15), "height": (8, 12)},
    "Stabilizer Link": {"length": (20, 35), "width": (5, 8), "height": (5, 8)},
    "Tie Rod": {"length": (25, 40), "width": (5, 8), "height": (5, 8)},
    "Steering Kit": {"length": (25, 35), "width": (15, 20), "height": (10, 15)},
}

def generate_dimensions(category):
    dims = DIMENSION_RANGES[category]
    length = round(random.uniform(*dims["length"]), 1)
    width = round(random.uniform(*dims["width"]), 1)
    height = round(random.uniform(*dims["height"]), 1)
    return length, width, height

parts = []
for i in range(500):
    number, category, brand = generate_part()
    sku = generate_sku(number,category,brand)
    weight = generate_weight(category)
    length, width, height = generate_dimensions(category)
    parts.append((number,category,brand,sku,weight,length,width,height))


df = pd.DataFrame(parts,columns=["number","category","brand","sku", "weight","length","width","height"])
print(df.head())
print(df.shape)
print(df.duplicated().sum())

df.to_csv("data/raw/parts.csv", index=False)

number,category,brand = generate_part()
print(generate_sku(number,category,brand))

