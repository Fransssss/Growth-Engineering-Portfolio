import pandas as pd

# syntetic dataset of users in A/B test
data = {
    'user_id': range(1,11),
    'group': ['control','control','control','control','control',
              'treatment','treatment','treatment','treatment','treatment'],
              'activated': [0,1,0,1,0,1,1,1,0,1],
              'country': ['US','US','UK','US','CA','US','UK','US','CA','US']
}

df = pd.DataFrame(data)

# view dataframe
print("Dataframe:")
print(df)

# filter for treatment group only
treatment = df[df['group'] == 'treatment']
print("\nTreatment Group:")
print(treatment)

# basic stats
print("\nTreatment Group Stats:")
print(treatment.describe())