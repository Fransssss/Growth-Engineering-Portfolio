import pandas as pd
import numpy as np
from scipy import stats
import hashlib
import matplotlib.pyplot as plt

np.random.seed(42)

# Simulate event pipeline
n_users = 1000

users = pd.DataFrame(
    {
        'user_id': range(1, n_users + 1),
        'signup_data': pd.date_range('2024-01-01', periods=n_users, freq='2h'),
        'country': np.random.choice(['US', 'UK', 'CA'], n_users, p=[0.6, 0.2, 0.2]),
        'plan': np.random.choice(['free', 'pro'], n_users, p=[0.85, 0.15])
    }
)
# Assignment service
def get_variant(user_id, experiment_id):
    hash_input = f"{user_id}_{experiment_id}".encode()
    hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
    return 'treatment' if hash_value % 2 == 0 else 'control'

users['variant'] = users['user_id'].apply(
    lambda uid: get_variant(
        uid,
        'retention_prompt_test'
    )
)

# Simulate events
events = []
for _, user in users.iterrows():
    # activation
    activation_prob = 0.52 if user['variant'] == 'treatment' else 0.42
    activated = np.random.binomial(1, activation_prob)

    if activated:
        events.append(
            {
                'user_id': user['user_id'],
                'event_name': 'sent_message',
                'variant': user['variant'],
                'day': 0
            }
        )

        # day 7 activation
        retention_prob = 0.28 if user['variant'] == 'treatment' else 0.22
        retained = np.random.binomial(1, retention_prob)
        if retained:
            events.append(
                {
                    'user_id': user['user_id'],
                    'event_name': 'returned_day7',
                    'variant': user['variant'],
                    'day': 7
                }
            )

events_df = pd.DataFrame(events)

# Analyze results
print("\n=== Experiment Results ===")

for metric in ['sent_message', 'returned_day7']:
    metric_df = events_df[events_df['event_name'] == metric]
    rates = metric_df.groupby('variant')['user_id'].nunique() / \
        users.groupby('variant')['user_id'].nunique()

    control_rate = rates.get('control',0)
    treatment_rate = rates.get('treatment',0)
    lift = treatment_rate - control_rate

    print(f"\n{metric}:")
    print(f" Control: {control_rate:.1%}")
    print(f" Treatment: {treatment_rate:.1%}")
    print(f" Lift: {lift:.2%}")


# SRM Check
print("\n=== SRM Check ===")
variant_counts = users['variant'].value_counts()
chi2, p_srm = stats.chisquare(
    [variant_counts.get('control',0),
     variant_counts.get('treatment', 0)],
     [n_users / 2, n_users / 2]
)

print(f"Split: {variant_counts.get('control')} control / {variant_counts.get('treatment')} treatment")
print(f"SRM p-value: {p_srm:.4f}")
print("OK: No SRM" if p_srm > 0.05 else "WARNING: SRM detected")

# Cohort retention by variant
activation_users = events_df[events_df['event_name'] == 'sent_message']['user_id']
retention_users = events_df[events_df['event_name'] == 'returned_day7']['user_id']

users['activated'] = users['user_id'].isin(activation_users).astype(int)
users['retained_day7'] = users['user_id'].isin(retention_users).astype(int)

summary = users.groupby('variant')[
    ['activated','retained_day7']
].mean()
print("\n=== Summary by Variant ====") 
print(summary.round(3))

# Plot 
fig, ax = plt.subplots(figsize=(8, 5))
metrics = ['activated', 'retained_day7']
x = np.arange(len(metrics))
width = 0.35 

control_vals = [summary.loc['control', m] for m in metrics]
treatment_vals = [summary.loc['treatment', m] for m in metrics]

ax.bar(x - width/2, control_vals, width, label='Control', color='#2196F3')
ax.bar(x + width/2, treatment_vals, width, label='Treatment', color='#FF7043')
ax.set_xticks(x)
ax.set_xticklabels(['Activation Rate', 'Day 7 Retention'])
ax.set_ylabel('Rate')
ax.set_title('Experiment Results: Control vs Treatment')
ax.legend()
plt.tight_layout()
plt.savefig('growth_system.png')
print("\nChart saved as growth_system.png\n")
