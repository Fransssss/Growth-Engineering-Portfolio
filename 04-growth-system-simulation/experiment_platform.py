import hashlib # so we can hash the experiment name to get a unique id
import pandas as pd # so we can save the results to a csv file
import numpy as np # so we can do some math
from scipy import stats # so we can do some statistical tests

# 1. Assignment Service
def get_variant(user_id, experimend_id, variants=['control','treatment']):
    hash_input = f"{user_id}_{experimend_id}".encode() # encode so we can hash it
    hash_value = int(hashlib.sha256(hash_input).hexdigest(),16) # use sha256 to get a hash value, convert to int
    return variants[hash_value % len(variants)]

# Test determinism - same user should always get same variant 
print("\n=== Assignment Service ===")
test_users = [101,202,303,404,505]
for uid in test_users:
    v1 = get_variant(uid, "welcome_prompt_test")
    v2 = get_variant(uid, "welcome_prompt_test")
    print(f"User {uid}: {v1} (consistent: {v1 == v2})")

# 2. Simulate experiment assignments for 1000 users
np.random.seed(42) # for reproducibility
n_users = 1000
user_ids = range(1, n_users+1)

assignments = pd.DataFrame(
    {
        'userid': user_ids,
        'variant': [get_variant(uid, "welcome_prompt_test") for uid in user_ids]
    }
)
    
assignment_counts = assignments["variant"].value_counts() # to check distribution
print("\n=== Assignment Counts ===")
print(assignment_counts)

# 3. SRM Detection
total = assignment_counts.sum() # so we can calculate percentages
expected = [ total / 2, total / 2] # so we can calculate expected counts
observed = [
    assignment_counts.get("control", 0),
    assignment_counts.get("treatment", 0)
]

chi2, p_value = stats.chisquare(observed, expected) # perform chi-squared test
print(f"\n=== SRM Check ===")
print(f"Expected split: {total//2} / {total//2}")
print(f"Observed split: {observed[0]} / {observed[1]}")
print(f"SRM p-value: {p_value:.4f}")

if p_value < 0.05:
    print("WARNING: SRM detected - do not analyze results")
else:
    print("OK: No SRM detected - experiment is valid for analysis")

# 4. Simulate a logging bug causing SRM 
print("\n=== Simulating SRM from logging bug ===")
# bug: 20% of treatment events fail to log, so we only see 80% of treatment users
buggy_assignments = assignments.copy() # this simulates the original assignments before the logging bug
treatment_mask = buggy_assignments["variant"] == "treatment" # this creates a mask that is True for treatment users and False for control users
drop_mask = treatment_mask & (np.random.random(n_users) < 0.20) # this creates a mask that is True for 20% of treatment users
buggy_assignments = buggy_assignments[~drop_mask] # this simulates the logging bug by dropping some treatment users

buggy_counts = buggy_assignments["variant"].value_counts() # to check distribution after the logging bug
observed_buggy = [
    buggy_counts.get("control", 0),
    buggy_counts.get("treatment", 0)
]
total_buggy = sum(observed_buggy) # so we can calculate expected counts after the logging bug
expected_buggy = [ total_buggy / 2, total_buggy / 2]

chi2, p_value = stats.chisquare(observed_buggy, expected_buggy) # so we can perform chi-squared test after the logging bug
print(f"Observed split: {observed_buggy[0]} / {observed_buggy[1]}")
print(f"SRM p-value: {p_value:.4f}")
if p_value < 0.05:
    print("WARNING: SRM detected - logging bug confirmed")
else:
    print("OK: No SRM detected")
