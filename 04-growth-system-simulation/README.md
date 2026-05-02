# Growth System Simulation - Claude.ai Growth

## Problem
Is the new onboarding features actually improving activation and retention, how do we measure it reliably end-to-end?

## Hypothesis
if 50% of new users are given a new onboarding feature, then activation rate and day 7 retention will increase compate to control, because the feature reduces friciton in the first session.

## Method
Used hashlib for Assignment service, simulated feature flag, detected SRM detection with scipy, measured activation and day 7 retention then visualization with matplotlib.

## Key Findings
- Treatment activation (53.1%) is 12.2 % more than control activation rate (40.9%)
- Treatment day 7 retention (16.6%) is 7% higher than control day day 7 retention (9.6%).
- Experiment is valid given clean SRM (501 control / 499 treatment)
- Both primary and secondary metrics moved in the right direction. 

## Recommendation
Ship the feature flag for new onboarding feature then figure out which specific setup drive the growth increase.

## Resume Bullet
Simulated end-to-end growth experiment including feature flag assignment, SRM detection, revealing +12.2pp activation and +7pp Day 7 retention lift using Python, hashlib, scipy and matplotlib. 