import pandas as pd
import numpy as np

def map_cibil(row):
    grade = row['loan_grade']
    
    # Using user provided ranges:
    # A: 800-900 (Exceptional)
    # B: 750-799 (Excellent)
    # C: 700-749 (Good)
    # D: 650-699 (Fair)
    # E: 600-649 (Doubtful/Low)
    # F & G: 300-599 (Poor/Very Low) - we'll split G as 300-449 and F as 450-599
    
    if grade == 'A':
        return np.random.randint(800, 901)
    elif grade == 'B':
        return np.random.randint(750, 800)
    elif grade == 'C':
        return np.random.randint(700, 750)
    elif grade == 'D':
        return np.random.randint(650, 700)
    elif grade == 'E':
        return np.random.randint(600, 650)
    elif grade == 'F':
        return np.random.randint(450, 600)
    elif grade == 'G':
        return np.random.randint(300, 450)
    else:
        return np.random.randint(600, 700) # Fallback

print("Loading original backup dataset (if available) or current dataset...")
try:
    df = pd.read_csv('data/credit_risk_dataset_backup.csv')
    print("Loaded from backup.")
except FileNotFoundError:
    df = pd.read_csv('data/credit_risk_dataset.csv')
    # Save a backup of the original dataset since we are dropping a column
    if 'loan_grade' in df.columns:
        df.to_csv('data/credit_risk_dataset_backup.csv', index=False)

if 'loan_grade' not in df.columns:
    print("Error: 'loan_grade' column not found! Revert to original dataset required.")
else:
    print("Mapping loan_grade to cibil_score...")
    np.random.seed(42)
    df['cibil_score'] = df.apply(map_cibil, axis=1)

    print("Dropping loan_grade...")
    df = df.drop(columns=['loan_grade'])

    print("Saving updated dataset...")
    df.to_csv('data/credit_risk_dataset.csv', index=False)
    print("Done! Dataset now contains 'cibil_score' using updated brackets.")
