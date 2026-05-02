import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def simulate_growth_loop( 
initial_users,
action_rate,
conversion_rate,
cycles,
label):
    """ Simulates a vrial growth loop over multiple cycles"""
    users = [initial_users]
    n = int(cycles)
    for cycle in range(n):
        current_users = users[-1] # -1 means the last element in the list
        new_users = current_users * action_rate * conversion_rate
        users.append(current_users + new_users)

        #print(f"cycles+1: {cycles + 1}, len(users): {len(users)}")
    return pd.DataFrame({
            'cycle': range(cycles + 1),
            'total_users': users,
            'label': [label] * len(users)
        })

# Base scenario
base = simulate_growth_loop(
    initial_users=10000,
    action_rate=0.05,
    conversion_rate=0.10,
    cycles=20,
    label='Base (5% actions, 10% conversion)'
)

# Improved action rate
improved_action = simulate_growth_loop(
    initial_users=10000,
    action_rate=0.08,
    conversion_rate=0.10,
    cycles=20,
    label='Improved action rate (8%)'
)

# Improved conversion rate
improved_conversion = simulate_growth_loop(
    initial_users=10000,
    action_rate=0.05,
    conversion_rate=0.16,
    cycles=20,
    label='Improved conversion rate (16%)'
)

# Print cycle 0, 5, 10, 20 for each scenario
print("=== Growth Loop Simulation ===")
print(f"{'Cycle':<8} {'Base':>12} {'Action+':>12} {'Convert+':>12}")
for cycle in [0, 5, 10, 20]:
    b = base[base['cycle'] == cycle]['total_users'].values[0]
    a = improved_action[improved_action['cycle'] == cycle]['total_users'].values[0]
    c = improved_conversion[improved_conversion['cycle'] == cycle]['total_users'].values[0]
    print(f"{cycle:<8} {b:>12,.0f} {a:12,.0f} {c:>12,.0f}")

# Plot
plt.figure(figsize=(10, 6))
for df in [base, improved_action, improved_conversion]:
    plt.plot(df['cycle'], df['total_users'], marker='o', markersize=3, label=df['label'].iloc[0])

plt.xlabel('Cycle')
plt.ylabel('Total Users')
plt.title('Growth Loop - Impact of Improving Action Rate vs Converstion Rate')
plt.legend()
plt.tight_layout()
plt.savefig('growth_loop.png')
print("\nChart saved as growth_loop.png\n")