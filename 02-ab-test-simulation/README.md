# A/B Test Simulation - Claude.ai Growth

## Problem
42% of new users who signed up never sent a first message. 
What change would increase the activation rate? 

## Hypothesis
if we suggest 3 prompts, then the activate rate will increase by 10% because users do not know what to ask and prompts remove that friction.

## Method
Simulated A/B test in Python using pandas for data manipulation,
scipy for chi-square significance testing, and statsmodels for sample size calculation. Tested 4,386 users (2,193 per group) over a 14-dayy test period.

## Key Findings
- Control activation rate: 43%
- Treatment activation rate: 53%
- Lift: +10 percentage points
- p-value: 0.0000 — statistically significant
- 95% CI: [6.7%, 12.6%] — entire interval above zero

## Recommendation
Ship the welcome message with 3 suggested prompts to newly signed up users. 
Next, run a new test to find out which of the 3 prompts drives the most activation.

## Resume Bullet
Designed and simulated an A/B test that results in +10% activation lift (43% -> 53%) with p < 0.05 using Python, scipy, pandas, 4386 simulated users.