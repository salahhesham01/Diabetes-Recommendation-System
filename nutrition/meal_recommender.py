def recommend_nutrition_plan(ranked_meals, calorie_target, user_diet, num_meals=4):
    if ranked_meals.empty:
        print("No meals available to recommend.")
        return None, 0

    # Define meal types and calorie ranges
    meal_types = {
        "Meal_1": (0.25 * calorie_target, 0.35 * calorie_target),  # e.g., 639–894 kcal for 2556 kcal
        "Meal_2": (0.30 * calorie_target, 0.40 * calorie_target),      # e.g., 767–1022 kcal
        "Meal_3": (0.25 * calorie_target, 0.35 * calorie_target),     # e.g., 639–894 kcal
        "Meal_4": (0.05 * calorie_target, 0.35 * calorie_target)       # e.g., 128–383 kcal
    }

    # Exclude non-meal cuisines
    excluded_cuisines = ["Beverages", "Cocktails", "Drinks", "Shakes", "Punch Beverage", "Bath/Beauty"]
    ranked_meals = ranked_meals[~ranked_meals["cuisine"].isin(excluded_cuisines)]

    plan = []
    total_calories = 0
    total_nutrients = {
        "carbs_g": 0, "protein_g": 0, "fat_g": 0, "fiber_g": 0, "sugar_g": 0,
        "cholesterol_g": 0, "sodium_g": 0, "saturatedFat_g": 0
    }
    used_meals = set()

    # Daily nutrient limits (scaled from user_diet, converted to mg where needed)
    daily_limits = {
        "carbs_g": user_diet["carb_max_g"] * num_meals,
        "fat_g": user_diet["fat_min_g"] * num_meals,
        "protein_g": user_diet["protein"] * num_meals,
        "fiber_g": user_diet["fiber_g"] * num_meals,
        "sugar_g": user_diet.get("sugar_g", 12) * num_meals,
        "cholesterol_g": user_diet["cholestrol_g"] * 1000 * num_meals,  # mg
        "sodium_g": user_diet["sodium_g"] * 1000 * num_meals,          # mg
        "saturatedFat_g": user_diet["saturated_fat"] * num_meals
    }

    # Select initial meals (Meal_1, Meal_2, Meal_3, and potentially Meal_4)
    for meal_type, (cal_min, cal_max) in list(meal_types.items())[:num_meals]:
        # Special handling for the fourth meal (Meal_4)
        if meal_type == "Meal_4":
            meal_candidates = ranked_meals[
                (ranked_meals["calories"] >= cal_min) &
                (ranked_meals["calories"] <= cal_max) &
                (~ranked_meals["meal_name"].isin(used_meals))
            ]

            if meal_candidates.empty:
                print(f"No suitable {meal_type} found within {cal_min:.0f}-{cal_max:.0f} kcal. Relaxing range.")
                cal_min = cal_min * 0.7
                cal_max = cal_max * 1.3
                meal_candidates = ranked_meals[
                    (ranked_meals["calories"] >= cal_min) &
                    (ranked_meals["calories"] <= cal_max) &
                    (~ranked_meals["meal_name"].isin(used_meals))
                ]

            if meal_candidates.empty:
                print(f"Still no {meal_type} found. Skipping.")
                continue

            # Check nutrient limits before adding Meal_4
            relaxed_limits = daily_limits.copy()
            # If total calories are below 95% of target and nutrients are near or at limits, relax limits
            if total_calories < 0.9 * calorie_target and any(
                total_nutrients[n] >= 0.9 * daily_limits[n] for n in total_nutrients
            ):
                print("Nutrient limits nearly exhausted and calories below 95% of target. Relaxing limits by 5%.")
                for nutrient in relaxed_limits:
                    relaxed_limits[nutrient] *= 1.05

            # Try to find a Meal_4 that fits within (possibly relaxed) limits
            Meal_4_added = False
            for _, meal in meal_candidates.iterrows():
                meal_nutrients = {
                    "carbs_g": meal["carbs_g"],
                    "protein_g": meal["protein_g"],
                    "fat_g": meal["fat_g"],
                    "fiber_g": meal["fiber_g"],
                    "sugar_g": meal["sugar_g"],
                    "cholesterol_g": meal["cholesterol_g"],
                    "sodium_g": meal["sodium_g"],
                    "saturatedFat_g": meal["saturatedFat_g"]
                }
                temp_nutrients = total_nutrients.copy()
                for nutrient, value in meal_nutrients.items():
                    temp_nutrients[nutrient] += value

                # Check if adding this meal exceeds limits (use relaxed_limits if applicable)
                limits_to_check = relaxed_limits if total_calories < 0.90 * calorie_target else daily_limits
                if all(temp_nutrients[n] <= limits_to_check[n] for n in temp_nutrients):
                    # Add the meal
                    plan.append({
                        "type": meal_type,
                        "meal_name": meal["meal_name"],
                        "cuisine": meal["cuisine"],
                        "calories": meal["calories"],
                        "carbs_g": meal["carbs_g"],
                        "protein_g": meal["protein_g"],
                        "fat_g": meal["fat_g"],
                        "fiber_g": meal["fiber_g"],
                        "sugar_g": meal["sugar_g"]
                    })
                    total_calories += meal["calories"]
                    used_meals.add(meal["meal_name"])
                    for nutrient, value in meal_nutrients.items():
                        total_nutrients[nutrient] += value
                    Meal_4_added = True
                    break
                elif total_calories < 0.9 * calorie_target:
                    # Try slight relaxation if meal would exceed original limits but calories are low
                    temp_relaxed_limits = daily_limits.copy()
                    for nutrient in temp_relaxed_limits:
                        temp_relaxed_limits[nutrient] *= 1.05  # 10% relaxation
                    if all(temp_nutrients[n] <= temp_relaxed_limits[n] for n in temp_nutrients):
                        print(f"Slightly relaxing limits by 10% to accommodate {meal_type}.")
                        relaxed_limits = temp_relaxed_limits
                        plan.append({
                            "type": meal_type,
                            "meal_name": meal["meal_name"],
                            "cuisine": meal["cuisine"],
                            "calories": meal["calories"],
                            "carbs_g": meal["carbs_g"],
                            "protein_g": meal["protein_g"],
                            "fat_g": meal["fat_g"],
                            "fiber_g": meal["fiber_g"],
                            "sugar_g": meal["sugar_g"]
                        })
                        total_calories += meal["calories"]
                        used_meals.add(meal["meal_name"])
                        for nutrient, value in meal_nutrients.items():
                            total_nutrients[nutrient] += value
                        Meal_4_added = True
                        break

            if not Meal_4_added:
                print(f"No suitable {meal_type} found within nutrient limits. Skipping.")
            continue

        # Handle Meal_1, Meal_2, and Meal_3
        meal_candidates = ranked_meals[
            (ranked_meals["calories"] >= cal_min) &
            (ranked_meals["calories"] <= cal_max) &
            (~ranked_meals["meal_name"].isin(used_meals))
        ]

        if meal_candidates.empty:
            print(f"No suitable {meal_type} found within {cal_min:.0f}-{cal_max:.0f} kcal. Relaxing range.")
            cal_min = cal_min * 0.7
            cal_max = cal_max * 1.3
            meal_candidates = ranked_meals[
                (ranked_meals["calories"] >= cal_min) &
                (ranked_meals["calories"] <= cal_max) &
                (~ranked_meals["meal_name"].isin(used_meals))
            ]

        if meal_candidates.empty:
            print(f"Still no {meal_type} found. Skipping.")
            continue

        # Select top-ranked meal
        meal = meal_candidates.iloc[0]
        meal_nutrients = {
            "carbs_g": meal["carbs_g"],
            "protein_g": meal["protein_g"],
            "fat_g": meal["fat_g"],
            "fiber_g": meal["fiber_g"],
            "sugar_g": meal["sugar_g"],
            "cholesterol_g": meal["cholesterol_g"],
            "sodium_g": meal["sodium_g"],
            "saturatedFat_g": meal["saturatedFat_g"]
        }

        plan.append({
            "type": meal_type,
            "meal_name": meal["meal_name"],
            "cuisine": meal["cuisine"],
            "calories": meal["calories"],
            "carbs_g": meal["carbs_g"],
            "protein_g": meal["protein_g"],
            "fat_g": meal["fat_g"],
            "fiber_g": meal["fiber_g"],
            "sugar_g": meal["sugar_g"]
        })
        total_calories += meal["calories"]
        used_meals.add(meal["meal_name"])
        for nutrient, value in meal_nutrients.items():
            total_nutrients[nutrient] += value

    # Check if total nutrients exceed daily limits (using relaxed limits if applicable)
    limits_to_check = relaxed_limits if 'relaxed_limits' in locals() else daily_limits
    for nutrient, total in total_nutrients.items():
        if total > limits_to_check[nutrient]:
            print(f"Warning: Total {nutrient} ({total:.1f}) exceeds limit ({limits_to_check[nutrient]:.1f}).")

    # Add extra Meal_4 if significant calorie shortfall and four meals are included
    if len(plan) >= 4 and total_calories < 0.90 * calorie_target:
        remaining_calories = calorie_target - total_calories
        meal_candidates = ranked_meals[
            (ranked_meals["calories"] >= 100) &
            (ranked_meals["calories"] <= remaining_calories) &
            (~ranked_meals["meal_name"].isin(used_meals))
        ]
        if not meal_candidates.empty:
            for _, meal in meal_candidates.iterrows():
                meal_nutrients = {
                    "carbs_g": meal["carbs_g"],
                    "protein_g": meal["protein_g"],
                    "fat_g": meal["fat_g"],
                    "fiber_g": meal["fiber_g"],
                    "sugar_g": meal["sugar_g"],
                    "cholesterol_g": meal["cholesterol_g"],
                    "sodium_g": meal["sodium_g"],
                    "saturatedFat_g": meal["saturatedFat_g"]
                }
                temp_nutrients = total_nutrients.copy()
                for nutrient, value in meal_nutrients.items():
                    temp_nutrients[nutrient] += value
                if all(temp_nutrients[n] <= limits_to_check[n] for n in temp_nutrients):
                    plan.append({
                        "type": "Extra Meal",
                        "meal_name": meal["meal_name"],
                        "cuisine": meal["cuisine"],
                        "calories": meal["calories"],
                        "carbs_g": meal["carbs_g"],
                        "protein_g": meal["protein_g"],
                        "fat_g": meal["fat_g"],
                        "fiber_g": meal["fiber_g"],
                        "sugar_g": meal["sugar_g"]
                    })
                    total_calories += meal["calories"]
                    for nutrient, value in meal_nutrients.items():
                        total_nutrients[nutrient] += value
                    break

    if not plan:
        print("Unable to generate a nutrition plan with the given constraints.")
        return None, 0

    return plan, total_calories


