import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Simulate 1000 users
n_users = 1000
users = pd.DataFrame({
    'user_id': range(1, n_users + 1),
    'signup_day': np.random.randint(1, 31, n_users),
    'country': np.random.choice(['US', 'UK', 'CA'], n_users, p=[0.6, 0.2, 0.2])
})

# Gradual rollout simulation
rollout_stages = [1, 10, 50, 100]
results = []

for pct in rollout_stages:
    exposed = ((users['user_id'] % 100) < pct).sum()
    results.append({
        'rollout_pct': pct,
        'users_exposed': exposed,
        'users_unexposed': n_users - exposed
    })

rollout_df = pd.DataFrame(results)
print("=== Gradual Rollout Simulation ===")
print(rollout_df.to_string(index=False))

# 50% rollout activation simulation
users['in_treatment'] = (users['user_id'] % 100) < 50

np.random.seed(42)
users['activated'] = np.where(
    users['in_treatment'],
    np.random.binomial(1, 0.52, n_users),
    np.random.binomial(1, 0.42, n_users)
)

activation = users.groupby('in_treatment')['activated'].agg(['mean', 'count']).reset_index()
activation['group'] = activation['in_treatment'].map({False: 'Control', True: 'Treatment'})
activation = activation[['group', 'mean', 'count']]
activation.columns = ['group', 'activation_rate', 'user_count']

print("\n=== 50% Rollout — Activation Results ===")
print(activation.round(3))

# Plot
plt.figure(figsize=(8, 4))
plt.plot(rollout_df['rollout_pct'], rollout_df['users_exposed'],
         marker='o', color='#2196F3')
plt.xlabel('Rollout Percentage (%)')
plt.ylabel('Users Exposed')
plt.title('Feature Flag — Gradual Rollout Progression')
plt.tight_layout()
plt.savefig('flag_rollout.png')
print("\nChart saved as flag_rollout.png\n")