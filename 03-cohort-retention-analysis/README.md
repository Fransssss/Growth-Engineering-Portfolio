# Cohort Retention Analysis - Claude.ai Growth

## Problem
It's unclear why retention is declining, whether the problem affects all users equally or only certian cohorts retain best and where is retention breaking down?

## Hypothesis
if onboarding prompting shipped in February and March worked then month 1 should become steadily improve across cohorts but the data shows April retention dropped back to 36.8% suggesting the improvement didn't hold.

## Method
Built cohort retention grid in Python using pandas for data manipulation and seaborn for heatmap visualization. Plotted day 0-30 retention curve using matplotlib. Analyzed funnel drop-off across 5 stages with 500 simulated users across 4 monthly cohorts (Janaury-April 2024).

## Key Findings
- February and March cohorts retained best at Month 1 (47.2%) vs January (41.6%) and April (36.8%)
- April retention dropped back to 36.8% despite onboarding improvements shipped in Feb/March
- Retention curve inflection point at Day 3 — 80% of churn happens before Day 7
- Retention floor stabilizes at 18% after Day 7
- Biggest funnel drop-off: 70% of users who signed up never sent a first message

## Recommendation
Analyze what the 18% of users who retained did differently in their first month. Run A/B test for 3 dayas with different prompt daily to get users to send at least one message a day because the data shows users who stays more than 3 days will retain better. 

## Resume Bullet
Analyzed 4-cohort retention grid identifying 80% churn before Day 7, 
18% retention floor, and declining Month 2 retention across cohorts 
using Python, pandas, seaborn, and matplotlib.