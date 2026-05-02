import numpy as np  # deal with numbers
import pandas as pd # deal with dataframes
from scipy import stats # deal with stats
import matplotlib.pyplot as plt # deal with plotting

np.random.seed(42) # for reproducibility -> meaning that every time we run this code, we will get the same random numbers, which is helpful for debugging and sharing results.

# Parameters from proposal
BASELINE_RATE = 0.42 # the current activation rate (42% of users activate)
TREATMENT_RATE = 0.52 # the expected activation rate with the new feature (52% of users activate)
SAMPLE_SIZE = 2192 # per group
TEST_DAYS = 14 # we will run the test for 14 days, and we expect to get 2192 users in each group during that time.

# simulate users
n = SAMPLE_SIZE

control_activated = np.random.binomial(1, BASELINE_RATE,n) # simulate control group (1 if activated, 0 if not) for n users, with a 42% chance of activation
treatment_activated = np.random.binomial(1, TREATMENT_RATE, n) # simulate treatment group (1 if activated, 0 if not) for n users, with a 52% chance of activation

# build dataframe
df = pd.DataFrame({
    'user_id': range(1,n*2+1),
    'group': ['control'] * n + ['treatment'] * n,
    'activated': list(control_activated) + list(treatment_activated)
})

# activation rates
rates = df.groupby('group')['activated'].mean()
print("=== Activation Rates ===")
print(rates)

# statistical test
contingency = pd.crosstab(df['group'], df['activated'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

print(f"\n=== Statistical Results ===")
print(f"Chi-square: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")
print(f"Result: {'Significant' if p_value < 0.05 else 'Not Significant'}")

# confidence intervals
control_rate = control_activated.mean() 
treatment_rate = treatment_activated.mean()
diff = treatment_rate - control_rate

se = np.sqrt(
    (control_rate * (1 - control_rate) / n ) +
     (treatment_rate * (1 - treatment_rate) / n)
    )

ci_lower = diff - 1.96 * se
ci_upper = diff + 1.96 * se

print(f"\n=== Effect Size ===")
print((f"Observed difference: +{diff:.1%}")) 
print(f"95% CI: [ {ci_lower:.1%}, {ci_upper:.1%} ]")

# daily activation over test period
daily_data = []
users_per_day = n // TEST_DAYS 

for day in range(1, TEST_DAYS + 1):
    start = (day - 1) * users_per_day 
    end = day * users_per_day 
    daily_data.append(
        {
            'day': day,
            'control': control_activated[start:end].mean(),
            'treatment': treatment_activated[start:end].mean()
        }
    )

    daily_df = pd.DataFrame(daily_data)

    plt.figure(figsize=(10,5))
    plt.plot(daily_df['day'], daily_df['control'], label='Control', marker='o')
    plt.plot(daily_df['day'], daily_df['treatment'], label='Treatment', marker='o')
    plt.axhline(y=BASELINE_RATE, color='gray', linestyle='--', alpha=0.5)
    plt.xlabel('Test Day')
    plt.ylabel('Activation Rate')
    plt.title('Daily Activation Rate: Control vs Treatment')
    plt.legend()
    plt.tight_layout()
    plt.savefig('activation_chart.png')
    print("\nChart saved as  activation_chart.png")
