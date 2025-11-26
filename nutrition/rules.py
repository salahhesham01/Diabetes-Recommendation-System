
def recommend_diet_with_expert_system(user_profile):

    bmi = float(user_profile.get("bmi", 25))
    diabetes_type = str(user_profile.get("diabetes_type", "0")) # "0": Prediabetes, "1": T1D, "2": LADA, "3": T2D, "4": MODY
    blood_glucose = float(user_profile.get("blood_glucose", 100))
    blood_pressure = float(user_profile.get("blood_pressure", 120))
    goal = user_profile.get("goal", "Blood sugar control") # "Weight loss", "Maintain weight"
    
    # Initialize scores for each diet
    scores = {
        "Dash": 0,
        "Mediterranean": 0,
        "Low-carb": 0,
        "Moderate-carb": 0,
        "Keto": 0
    }

    # --- Rule 1: High Blood Pressure ---
    # The DASH diet is specifically designed to manage hypertension.
    if blood_pressure > 130:
        scores["Dash"] += 3.0 # Strong recommendation
        scores["Mediterranean"] += 1.0 # Also good for heart health

    # --- Rule 2: Weight Status and Goals ---
    # Keto and Low-carb diets are often effective for significant weight loss.
    if bmi >= 30: # Obesity
        if goal == "Weight loss":
            scores["Keto"] += 2.5 # Strong recommendation for weight loss goal
            scores["Low-carb"] += 2.0
        else:
            scores["Low-carb"] += 1.5
            scores["Mediterranean"] += 1.0
    elif 25 <= bmi < 30: # Overweight
        if goal == "Weight loss":
            scores["Low-carb"] += 2.0
            scores["Mediterranean"] += 1.5

    # --- Rule 3: Diabetes Type Specifics ---
    # Different diabetes types have different nutritional needs.
    
    # For Type 2 Diabetes (often linked to lifestyle and weight)
    if diabetes_type == "3":
        if bmi >= 25: # Overweight or Obese
             scores["Low-carb"] += 2.0
             scores["Mediterranean"] += 1.5
        else: # Normal weight
            scores["Moderate-carb"] += 1.5
            scores["Mediterranean"] += 1.0

    # For Type 1 Diabetes and LADA (autoimmune, focus on carb management)
    # Keto is generally discouraged due to ketoacidosis risk.
    if diabetes_type in ["1", "2"]:
        scores["Moderate-carb"] += 2.0 # Consistent carb intake is key
        scores["Low-carb"] += 1.0
        scores["Keto"] -= 1.0 # Contraindication

    # For Prediabetes (focus on prevention and reversal)
    if diabetes_type == "0":
        scores["Mediterranean"] += 2.5 # Excellent for prevention
        scores["Dash"] += 1.5
        scores["Low-carb"] += 1.0

    # For MODY (genetic, often managed like T1D or T2D depending on the specific gene)
    if diabetes_type == "4":
        scores["Moderate-carb"] += 2.0
        scores["Mediterranean"] += 1.5

    # --- Rule 4: Blood Glucose Level ---
    # Higher glucose levels may warrant stricter carb control.
    if blood_glucose > 180: # Significantly high
        scores["Low-carb"] += 1.5
        scores["Keto"] += 1.0
    elif 126 <= blood_glucose <= 180: # Elevated
        scores["Low-carb"] += 1.0
        scores["Moderate-carb"] += 0.5

    # If no diet has a positive score, default to a safe option
    if max(scores.values()) <= 0:
        return "Mediterranean"

    # Return the diet with the highest score
    recommended_diet = max(scores, key=scores.get)
    return recommended_diet