import pandas as pd 
from scipy import stats

# dataset
data = {
    'user_id': range(1,101),
    'group':['control'] * 50 + ['treatment'] * 50,
    'activated' : [0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,0,0,
                  1,0,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,
                  0,1,0,1,0,0,1,0,1,0,
                  1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,0,1,
                  1,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,
                  0,1,1,1,0,1,1,1,1,0]
}

df = pd.DataFrame(data)

# activation rate per group
activation_rates = df.groupby('group')['activated'].mean()
print("\nActivation Rates:")
print(activation_rates)

# split into control and treatment 
control = df[df['group'] == 'control']['activated']
treatment = df[df['group'] == 'treatment']['activated']

# run a two-proportion z-test
control_activated = control.sum()
treatment_activated = treatment.sum() 
control_total = len(control)
treatmnet_total = len(treatment)

# chi-square test
contingency_table = pd.crosstab(df['group'],df['activated'])
print("\nContingency table:")
print(contingency_table)

chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"\nChi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.4f}\n")

if p_value < 0.05:
    print("Result: Statistically significant")
else:
    print("Result: Not statistically significant")

print('\n')