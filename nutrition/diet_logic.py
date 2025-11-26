def select_diet(user_profile, choice, manual_diet=None, calorie_target=2000):
    diets = {
        "Low-carb": {
            "name": "Low-carb", "carb_max_g": 20, "fat_min_g": 40, "protein": 20,
            "saturated_fat": 6, "fiber_g": 30, "cholestrol_g": 0.15, "sodium_g": 2.3
        },
        "Mediterranean": {
            "name": "Mediterranean", "carb_max_g": 40, "fat_min_g": 30, "protein": 30,
            "saturated_fat": 8, "fiber_g": 30, "cholestrol_g": 0.2, "sodium_g": 2, "cuisine": "Mediterranean"
        },
        "Keto": {
            "name": "Keto", "carb_max_g": 5, "fat_min_g": 75, "protein": 25,
            "saturated_fat": 10, "fiber_g": 17.5, "cholestrol_g": 0.4, "sodium_g": 3
        },
        "Moderate-carb": {
            "name": "Moderate-carb", "carb_max_g": 35, "fat_min_g": 30, "protein": 35,
            "saturated_fat": 7, "fiber_g": 30, "cholestrol_g": 0.25, "sodium_g": 2.3
        },
        "Dash": {
            "name": "Dash", "carb_max_g": 60, "fat_min_g": 27, "protein": 18,
            "saturated_fat": 6, "fiber_g": 30, "cholestrol_g": 0.15, "sodium_g": 2.3
        }
    }
    for diet in diets.values():
        diet["carb_max_g"] = (diet["carb_max_g"] / 100 * calorie_target) / 4 / 4
        diet["fat_min_g"] = (diet["fat_min_g"] / 100 * calorie_target) / 9 / 4
        diet["protein"] = (diet["protein"] / 100 * calorie_target) / 4 / 4
        diet["saturated_fat"] = (diet["saturated_fat"] / 100 * calorie_target) / 9 / 4
    
    selected_diet = diets[manual_diet]
 
    return selected_diet
