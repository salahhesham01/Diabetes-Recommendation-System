# Diabetes Type Prediction & Nutrition Recommendation System

This project predicts the **type of diabetes** for a patient using machine learning and recommends a **personalized nutrition plan** based on the predicted type.  

The system combines **Random Forest classification** for predicting diabetes type and a **rule-based + similarity scoring** method for recommending suitable diets.  



## Overview

The system has **two main components**:  

1. **Diabetes Type Prediction**  
   - Uses patient-specific features (e.g., age, BMI, glucose levels)  
   - Predicts the type of diabetes (Type 1, Type 2, or other) using **Random Forest Classifier**  

2. **Nutrition Recommendation**  
   - Selects suitable diet types based on **rule-based conditions**  
   - Chooses the best matching diet plan using **cosine similarity** between patient needs and diet nutritional profiles  
   - Provides a personalized list of recommended meals
  
3. **User Interface**  
   - Built using **Streamlit**  
   - Allows users to input patient data and view predicted diabetes type and recommended meals  

---

## Dataset

- **Diabetes dataset**: Includes medical and lifestyle features for patients.  
- **Nutrition/Recipes dataset**: Contains diet types, recipes, and nutritional information.  
- **Sources**: Kaggle and Food.com
---

## Data Preprocessing

- Handle missing values and duplicates  
- Scale numerical features using MinMaxScaler  
- Encode categorical variables using LabelEncoder  
- Generate additional features if needed (e.g., BMI categories)  

---

## Modeling

- **Model**: Random Forest Classifier  
- **Target**: Diabetes type  
- **Evaluation Metric**: Accuracy, F1-score, Confusion Matrix  
- **Output**: Predicted diabetes type for each patient  

---

## Nutrition Recommendation

- **Step 1: Rule-based filtering**  
  - Select diet types suitable for the predicted diabetes type  

- **Step 2: Similarity scoring**  
  - Compute **cosine similarity** between patient nutritional needs and diet features  
  - Rank diets and select the most suitable meal plans  

- **Step 3: Recommendation**  
  - Display personalized recommended meals  

---

## Streamlit UI

- Users can input patient data in a **simple form**  
- System outputs:
  1. Predicted diabetes type  
  2. Recommended diet plans
     
<img width="773" height="338" alt="image" src="https://github.com/user-attachments/assets/f6941311-188a-4e77-8eb7-d410c3bb0d94" />

<img width="802" height="355" alt="image" src="https://github.com/user-attachments/assets/8abbebd8-9b44-4b71-9df3-cbca0278e6cb" />

<img width="700" height="311" alt="image" src="https://github.com/user-attachments/assets/35280e9b-d68e-4344-a1e8-c02447fee61e" />

<img width="713" height="312" alt="image" src="https://github.com/user-attachments/assets/4d2294b8-0233-4b31-9dbc-effe03c00890" />

<img width="710" height="306" alt="image" src="https://github.com/user-attachments/assets/dfcf8044-94d5-4149-9611-13a4518fe851" />

<img width="707" height="314" alt="image" src="https://github.com/user-attachments/assets/1bbcdd6e-f130-4b11-b4a0-a971b6110d31" />

<img width="709" height="315" alt="image" src="https://github.com/user-attachments/assets/f56ef7b8-cef5-4664-82a2-9b9ae694300e" />

<img width="708" height="319" alt="image" src="https://github.com/user-attachments/assets/0f6c9239-bdb6-4fdd-88fd-58edbcca5112" />

<img width="703" height="308" alt="image" src="https://github.com/user-attachments/assets/c4d41381-c388-4f5d-b832-5bed550c066a" />




