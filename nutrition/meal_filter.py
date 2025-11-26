
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
def filter_meals(user_profile, user_goal, user_diet):
    """Filter recipes based on diet criteria from select_diet, user constraints, and allergies."""
    df = pd.read_csv("nutrition/data/processed_recipes.csv")

    # Initialize filtering conditions
    filtered_df = df.copy()

    # Apply nutritional constraints from user_diet (from select_diet)
    filtered_df = filtered_df[
        (filtered_df["carbs_g"] <= user_diet["carb_max_g"] * 1.5 ) &  # Relax to 1.5x for flexibility
        (filtered_df["fat_g"] <= user_diet["fat_min_g"]*1.5) &  # Allow 0.8x flexibility
        (filtered_df["protein_g"] <= user_diet["protein"] *1.5) &  # Ensure sufficient protein
        (filtered_df["fiber_g"] <= user_diet["fiber_g"]*1.5 ) &  # Minimum fiber
        (filtered_df["sugar_g"] <= 12) &  # Default sugar limit if not specified
        (filtered_df["cholesterol_g"] <= user_diet["cholestrol_g"] * 1000 *1.5) &  # Convert g to mg, relax 1.2x
        (filtered_df["sodium_g"] <= user_diet["sodium_g"] * 1000*1.5 ) &  # Convert g to mg, relax 1.2x
        (filtered_df["saturatedFat_g"] <= user_diet["saturated_fat"]*1.5 )  # Relax saturated fat 1.2x
    ]
    # Ensure at least some meals are returned
    if filtered_df.empty:
        print("Warning: Still no meals found after relaxing filters. Consider adjusting diet constraints or user preferences.")

    return filtered_df

def rank_meals_cosine(filtered_meals, user_diet):
    """Rank meals based on cosine similarity with diet nutrient profile."""
    if filtered_meals.empty:
        print("No meals to rank.")
        return filtered_meals

    # Nutrients to compare
    nutrient_cols = [
        "carbs_g", "protein_g", "fat_g", "fiber_g",
        "saturatedFat_g", "cholesterol_g", "sodium_g", "sugar_g"
    ]

    # Build diet vector and normalize units where necessary (e.g., cholesterol and sodium in mg)
    diet_vector = np.array([
        user_diet["carb_max_g"],
        user_diet["protein"],
        user_diet["fat_min_g"],
        user_diet["fiber_g"],
        user_diet["saturated_fat"],
        user_diet["cholestrol_g"] * 1000,  # convert g to mg
        user_diet["sodium_g"] * 1000,      # convert g to mg
        user_diet.get("sugar_g", 12)
    ]).reshape(1, -1)

    # Prepare meal matrix
    meal_matrix = filtered_meals[nutrient_cols].values

    # Scale both meal data and diet vector
    scaler = StandardScaler()
    meal_matrix_scaled = scaler.fit_transform(meal_matrix)
    diet_vector_scaled = scaler.transform(diet_vector)

    # Compute cosine similarity
    similarities = cosine_similarity(meal_matrix_scaled, diet_vector_scaled).flatten()

    # Add similarity scores to meals
    filtered_meals = filtered_meals.copy()
    filtered_meals["score"] = similarities

    # Rank meals by similarity
    ranked_meals = filtered_meals.sort_values(by="score", ascending=False)
    return ranked_meals.drop(columns=["score"])