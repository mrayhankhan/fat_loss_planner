import numpy as np

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_daily_calories(current_weight, target_weight, weeks, bmr, activity_factor):
    weight_loss_needed = current_weight - target_weight
    calorie_deficit_needed = weight_loss_needed * 7700
    daily_calorie_deficit = calorie_deficit_needed / (weeks * 7)
    
    # Calculate TDEE
    tdee = bmr * activity_factor
    
    # Check for impossible target weight
    if daily_calorie_deficit > tdee:
        return {
            "TDEE": tdee,
            "Daily Calorie Deficit": "Impossible target weight in given weeks. Please adjust your target weight or time frame."
        }
    
    return {
        "TDEE": tdee,
        "Daily Calorie Deficit": daily_calorie_deficit
    }

def estimate_body_composition(weight, height, bmi, gender):
    # Placeholder function for body composition estimation
    lean_mass = weight * 0.8  # Example calculation
    fat_mass = weight * 0.2   # Example calculation
    return {"lean_mass": lean_mass, "fat_mass": fat_mass}