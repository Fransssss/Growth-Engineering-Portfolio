import pandas as pd # deal with dataframes
import numpy as np # deal with arrays and random numbers
import matplotlib.pyplot as plt # deal with plotting
import seaborn as sns # deal with advanced plotting

np.random.seed(42) # why? for reproducibility -> meaning that every time we run this code, we will get the same random numbers, which is helpful for debugging and sharing results.

# simulate user signup and activity data 
n_users = 500
cohort_months = [
    '2024-01', '2024-02', '2024-03', '2024-04'
]
users_per_cohort = n_users // len(cohort_months)

records = []
for cohort_idx, cohort in enumerate(cohort_months):
    # retention declines slightly for later cohorts
    base_retention = 0.45 - cohort_idx * 0.03

    for user in range(users_per_cohort):
        user_id = cohort_idx * users_per_cohort + user 
        for month in range(4):
            if month == 0: 
                active = 1
            else:
                # retention probability decays over time
                prob = base_retention * (0.75 ** (month - 1))
                active = np.random.binomial(1,prob)
            
            if active:
                records.append(
                    {
                        'user_id': user_id,
                        'cohort': cohort,
                        'month_number': month
                    }
                )

df = pd.DataFrame(records) # creating a dataframe from the records list, which contains dictionaries of user activity data. Each dictionary has keys 'user_id', 'cohort', and 'month_number', and the corresponding values represent the user's ID, the cohort they belong to, and the month number of their activity.

# build cohort grid
cohort_sizes = df[
    df['month_number'] == 0
].groupby('cohort')['user_id'].nunique() #  calculating the size of each cohort by counting the number of unique users in the first month (month_number == 0) for each cohort. It groups the data by 'cohort' and then counts the unique 'user_id' values to get the number of users in each cohort.

cohort_activity = df.groupby(
    ['cohort', 'month_number'])['user_id'].nunique().reset_index()

cohort_activity_columns = [
    'cohort',
    'month_number',
    'active_users'
]

# merge cohort sizes
cohort_sizes_df = cohort_sizes.reset_index()
cohort_sizes_df.columns = ['cohort', 'cohort_size']
cohort_activity = cohort_activity.merge(cohort_sizes_df, on='cohort')

cohort_activity = cohort_activity.rename(columns={'user_id': 'active_users'})

# print(cohort_activity.columns.tolist())  # debug
# print(cohort_activity.head())            # debug

cohort_activity['retention_rate'] = (
    cohort_activity['active_users'] / cohort_activity['cohort_size']
)

# pivot to grid format
cohort_grid = cohort_activity.pivot(
    index='cohort',
    columns='month_number',
    values='retention_rate'
)
cohort_grid.columns = [
    f'Month {m}' for m in cohort_grid.columns
]

print("\n=== Cohort Retention Grid ===")
print(
    (cohort_grid * 100).round(1).to_string()
)

# heatmap
plt.figure(figsize=(8,5))
sns.heatmap(
    cohort_grid * 100,
    annot=True,
    fmt='.1f',
    cmap='YlOrRd_r',
    vmin=0,
    vmax=100,
    linewidths=0.5
)
plt.title('Claud.ai - Cohort Retention Heatmap (%)')
plt.ylabel('Cohort (Signup Month)')
plt.xlabel('Months Since Signup')
plt.tight_layout()
plt.savefig('cohort_heatmap.png')
print("\nHeatmap saved as cohort_heatmap.png\n")