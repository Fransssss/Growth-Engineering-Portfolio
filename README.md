# User Funnel Analysis - Claude.ai Growth

## Hypothesis
Users are dropping off between activation and revenue conversion.

## Method
SQL funnel analysis on user_events table (SQLite)

## Findings
- 10 users analyzed
- 70% activation rate (sent_message)
- 30% revenue conversion rate (upgraded_to_pro)
- Biggest drop-off: activation → revenue

## Recommendation
Investigate session depth differences between converters and non-converters.

## Resume Bullet
- Analyzed 10-user onboarding funnel revealing 70% activation rate and 30% revenue conversion rate using SQL, identifying drop-off between activation and revenue 
as the primary growth opportunity.

- Designed and executed an A/B test simulation in Python revealing a 10 percentage point activation rate lift (43% → 53%) across 4,386 simulated users using scipy and pandas.

- Built end-to-end retention analysis across 4 user cohorts using Python, identifying 70% activation drop-off and declining Month 2 retention, and recommended a Day 1 prompt sequence A/B test to raise the retention floor.
