def get_skincare_recommendations(skin_type, concerns):
    recommendations = {
        'normal': [
            "Use a gentle cleanser twice daily",
            "Apply a light moisturizer",
            "Use sunscreen daily"
        ],
        'dry': [
            "Use a creamy, non-foaming cleanser",
            "Apply a rich moisturizer",
            "Consider using facial oils",
            "Use a hydrating sunscreen"
        ],
        'oily': [
            "Use a foaming cleanser",
            "Apply a light, oil-free moisturizer",
            "Use oil-control products",
            "Choose non-comedogenic sunscreen"
        ],
        'combination': [
            "Use different products for different areas of your face",
            "Consider using a toner",
            "Apply moisturizer more heavily on dry areas",
            "Use a balanced sunscreen"
        ],
        'sensitive': [
            "Use hypoallergenic products",
            "Avoid fragrances and harsh chemicals",
            "Apply a soothing moisturizer",
            "Use physical sunscreens (zinc oxide or titanium dioxide)"
        ]
    }
    
    concern_recommendations = {
        'acne': ["Use salicylic acid or benzoyl peroxide products", "Avoid heavy, oily products"],
        'aging': ["Use retinol products", "Apply products with antioxidants"],
        'hyperpigmentation': ["Use products with vitamin C", "Apply skin-lightening products"],
        'dryness': ["Use a humidifier", "Apply hyaluronic acid serums"],
    }
    
    result = recommendations.get(skin_type, [])
    for concern in concerns.lower().split(','):
        concern = concern.strip()
        if concern in concern_recommendations:
            result.extend(concern_recommendations[concern])
    
    return result

def get_diet_recommendations(skin_type, concerns):
    general_recommendations = [
        "Drink plenty of water",
        "Eat a balanced diet rich in fruits and vegetables",
        "Consume foods high in omega-3 fatty acids (e.g., fish, flaxseeds)",
        "Limit sugar and processed foods"
    ]
    
    specific_recommendations = {
        'dry': ["Increase healthy fats (avocados, nuts)", "Eat foods rich in vitamin E"],
        'oily': ["Reduce dairy intake", "Eat more zinc-rich foods (pumpkin seeds, lean meats)"],
        'sensitive': ["Avoid spicy foods", "Consume anti-inflammatory foods (berries, leafy greens)"],
        'acne': ["Limit high-glycemic foods", "Increase probiotics (yogurt, kefir)"],
        'aging': ["Eat more antioxidant-rich foods (berries, dark chocolate)", "Increase collagen-boosting foods (bone broth, citrus fruits)"],
    }
    
    result = general_recommendations.copy()
    result.extend(specific_recommendations.get(skin_type, []))
    for concern in concerns.lower().split(','):
        concern = concern.strip()
        if concern in specific_recommendations:
            result.extend(specific_recommendations[concern])
    
    return list(set(result))  # Remove duplicates