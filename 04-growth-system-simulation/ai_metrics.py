import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

np.random.seed(0) # reproducibility means that the same random numbers are generated each time

# Simulate 500 users sessions
n_sessions = 500

sessions = pd.DataFrame(
    {
        'session_id': range(1, n_sessions + 1),
        'user_id': np.random.randint(1, 101, n_sessions),
        'message_sent': np.random.choice(
            [1,2,3,4,5,6,7,8,9,10], n_sessions, 
            p = [0.30, 0.25, 0.15, 0.10, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01]
        ),
        'copied_response': np.random.binomial(1,0.35,n_sessions),
        'regenerated': np.random.binomial(1,0.20,n_sessions),
        'abandoned': np.random.binomial(1,0.25,n_sessions),
        'explicit_negative': np.random.binomial(1, 0.05, n_sessions)
    }
)

# Session depth classification
sessions['depth_category'] = pd.cut(
    sessions['message_sent'],
    bins=[0, 2, 6,10],
    labels=['Shallow', 'Medium', 'Deep']
)

# Task completion score 
sessions['completion_score'] = (
    0.4 * sessions['copied_response'] +
    0.3 * (1 - sessions['abandoned']) +
    0.2 * (sessions['message_sent'] > 2).astype(int) +
    0.1 * (1 - sessions['explicit_negative'])
)

print("\n=== Session Depth distribution ===")
depth_dist = sessions['depth_category'].value_counts()
print(depth_dist)

print("\n=== Average Completion Score by Depth ===")
completion_by_depth = sessions.groupby('depth_category', observed=True)['completion_score'].mean()
print(completion_by_depth.round(3))

print("\n=== Hallucination Signals ===")
print(f"Regeneration rate: {sessions['regenerated'].mean():.1%}")
print(f"Abandonment rate: {sessions['abandoned'].mean():.1%}")
print(f"Explicit negative rate: {sessions['explicit_negative'].mean():.1%}")
print(f"Overall quality score: {1 - sessions['regenerated'].mean() - sessions['explicit_negative'].mean():.1%}")

print("\n=== North Start Metrics ===")
# User with 3+ message session this week
north_star_users = sessions[sessions['message_sent'] >=3]['user_id'].nunique()
total_users = sessions['user_id'].nunique()
print(f"Users with 3+ message sessions: {north_star_users} / {total_users} ({north_star_users / total_users:.1%})")

# Plot session depth distribution
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Chart 1: Session depth
depth_dist.plot(kind='bar', ax=axes[0], color=['#EF5350', '#FFA726', '#66BB6A'])
axes[0].set_title("Session Depth Distribution")
axes[0].set_xlabel("Depth Category")
axes[0].set_ylabel("Number of Sessions")
axes[0].tick_params(axis='x', rotation=0)

# Chart 2: Completion score by depth
completion_by_depth.plot(kind='bar', ax=axes[1], color=['#EF5350', '#FFA726', '#66BB6A'])
axes[1].set_title("Average Completion Score by Session Depth")
axes[1].set_xlabel("Depth Category")
axes[1].set_ylabel("Completion Score")
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig("ai_metrics.png")
print("\nCharts saved as 'ai_metrics.png'\n")