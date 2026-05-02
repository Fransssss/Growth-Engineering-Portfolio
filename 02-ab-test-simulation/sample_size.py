import pandas as pd # for data manipulation
import numpy as np # for numerical operations
from scipy import stats # for chi-square test
from statsmodels.stats.proportion import proportions_ztest # for two-proportion z-test
import statsmodels.stats.api as sms # for power analysis

# 1. sample size calculation
baseline_rate = 0.42  # current activation rate
mde = 0.10           # minimum detectable effect (10% increase)
expected_rate = baseline_rate * (1 + mde) # expected activation rate in treatment group

effect_size = sms.proportion_effectsize(baseline_rate, expected_rate)
sample_size = sms.NormalIndPower().solve_power(
    effect_size,            # effect size based on baseline and expected rates
    power=0.80,             # how often to see real effect if it exists
    alpha=0.05,             # false alarm
    alternative='two-sided' # difference
)

print("\n== Sample Size Calculation ==")
print(f"Baseline activation rate: {baseline_rate:.0%}") # % of users activate without any changes.
print(f"Expected treatment rate: {expected_rate:.0%}")     # If the experiment works, I hope activation goes up to this
print(f"Require sample size per group: {int(np.ceil(sample_size))}") # Number of sample size required to reliably detect a jump from 42% → 46%, in control AND in treatment.”
print(f"Total users needed: {int(np.ceil(sample_size)) * 2}\n") # Total users needed across both groups.

# 2. Confidence internval on previous day (p-value and statistical significance))
control_activated = 21
control_total = 50
treatment_activated = 37
treatment_total = 50

control_rate = control_activated / control_total
treatment_rate = treatment_activated / treatment_total
diff = treatment_rate - control_rate

# standard error of the difference
se = np.sqrt(
    (control_rate * (1- control_rate) / control_total) +
    (treatment_rate * (1 - treatment_rate) / treatment_total)
)

ci_lower = diff - 1.96 * se
ci_upper = diff + 1.96 * se 

print(f"== Confidence Interval ==")
print(f"Control activation rate: {control_rate:.0%}")
print(f"Treatment activation rate: {treatment_rate:.0%}")
print(f"Observed difference: +{diff:.0%}") 
print(f"95% Confidence Interval: [{ci_lower:.0%}, {ci_upper:.0%}]")
