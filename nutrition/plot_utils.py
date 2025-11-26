import pandas as pd
import plotly.express as px

def plot_nutrients(plan):
    if not plan:
        return None
    df = pd.DataFrame(plan)
    return px.bar(df, x="type", y=["carbs_g", "protein_g", "fat_g"],
                  title="Nutrient Breakdown per Meal",
                  labels={"value": "Grams", "variable": "Nutrient"})
