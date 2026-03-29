import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

np.random.seed(0) # for reproducibility

# simulate 1000 users with daily retention probabilities
n_users = 1000
days = 30

# retention probablity per day - decays over time then stabilizes
retention_probs = np.array(
    [
        1.0, # day 0, all users are active
        0.45, # day 1
        0.35, # day 2
        0.28, # day 3
        0.24, # day 4
        0.22, # day 5
        0.21, # day 6
        0.20, # day 7
    ] + [
        max(0.18, 0.20 - i * 0.002) for i in range(23) # gradual decay to floor
    ]
)

# build retention curve
retention_curve = []

for day, prob in enumerate(retention_probs):
    active_users = int(n_users * prob)
    retention_curve.append(
        {
            'day': day,
            'active_users': active_users,
            'retention_rate': prob
        }
    )

    df = pd.DataFrame(retention_curve)

    print("\n=== Retention Curve Data ===")
    print(df[
        ['day','active_users','retention_rate']
        ].to_string(index=False)
    )

    # plot 
    plt.figure(figsize=(10,5))
    plt.plot(df['day'], df['retention_rate'] * 100, marker='o', markersize=4)
    plt.axvline(x=3, color='red', linestyle='--', label='Inflection Point (Day 3)')
    plt.axhline(y=18, color='green', linestyle='--', alpha=0.5, label='Retention floor (18%)')
    plt.xlabel('Days Since First Session')
    plt.ylabel('% Users Still Active')
    plt.title('Claude.ai - Day 0-30 Retention Curve')
    plt.legend()
    plt.tight_layout()
    plt.savefig('retention_curve.png')
    print("\nChart saved as retention_curve.png\n")
