def calculate_calories(user_profile, user_goal):
    """Calculate daily calorie needs using Mifflin-St Jeor Equation."""
    weight = user_profile["weight_kg"]
    height = user_profile["height_cm"]
    age = user_profile["age"]
    if user_profile["gender"] == "M":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    activity_factors = {
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    tdee = bmr * activity_factors[user_profile["activity_level"]]
    calorie_target = tdee + user_goal["calorie_adjustment"]
    return round(calorie_target)
