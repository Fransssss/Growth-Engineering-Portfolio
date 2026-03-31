import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Claude.ai activation funnel data
funnel_data = {
    'stage': [
        'Landed on page',
        'Clicked sign up',
        'Completed signup',
        'Sent first message',
        'Sent 3+ messages'
    ],
    'users': [10000, 6000, 4000, 1200, 480]
}

df = pd.DataFrame(funnel_data)

# Calculate drop-off metrics
df['conversion_rate'] = df['users'] / df['users'].iloc[0] * 100
df['step_conversion'] = df['users'] / df['users'].shift(1) * 100
df['users_lost'] = df['users'].shift(1) - df['users']
df['dropoff_rate'] = df['users_lost'] / df['users'].shift(1) * 100

print("=== Funnel Drop-off Analysis ===")
cols = ['stage', 'users', 'step_conversion', 'dropoff_rate']
print(df[cols].to_string(index=False))

# Identify biggest drop-off
biggest_dropoff_idx = df['users_lost'].idxmax()
biggest_dropoff = df.loc[biggest_dropoff_idx, 'stage']
print(f"\nBiggest drop-off stage: {biggest_dropoff}")
print(f"Users lost: {int(df.loc[biggest_dropoff_idx, 'users_lost'])}")
print(f"Drop-off rate: {df.loc[biggest_dropoff_idx, 'dropoff_rate']:.1f}%")

# Funnel chart
fig, ax = plt.subplots(figsize=(10, 7))

colors = ['#2196F3', '#42A5F5', '#EF5350', '#E53935', '#B71C1C']
max_users = df['users'].iloc[0]

for i, (_, row) in enumerate(df.iterrows()):
    width = row['users'] / max_users
    bar_height = 0.6
    y_pos = len(df) - i - 1

    ax.barh(y_pos, width, height=bar_height,
            color=colors[i], alpha=0.85)

    ax.text(width + 0.01, y_pos,
            f"{int(row['users']):,} users",
            va='center', fontsize=10)

    if i > 0:
        dropoff = row['dropoff_rate']
        ax.text(0.5, y_pos + 0.5,
                f"▼ {dropoff:.0f}% drop-off",
                ha='center', va='center',
                fontsize=9, color='red', alpha=0.7)

ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['stage'][::-1], fontsize=11)
ax.set_xlim(0, 1.3)
ax.set_xlabel('Proportion of Total Users')
ax.set_title('Claude.ai — Activation Funnel Drop-off Analysis')
ax.axvline(x=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig('funnel_dropoff.png')
print("\nFunnel chart saved as funnel_dropoff.png")