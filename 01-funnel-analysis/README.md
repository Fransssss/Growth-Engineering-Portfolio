# User Funnel Analysis - Claude.ai Growth

## Problem
58% of new users never send a first message after signing up. 
Where exactly is the funnel breaking down?

## Hypothesis
Users are dropping off between activation and revenue conversion, 
not at the top of the funnel.

## Method
SQL funnel analysis on user_events table (SQLite) using 
COUNT DISTINCT, GROUP BY, and LEFT JOIN to measure drop-off 
at each funnel stage.

## Findings
- 10 users analyzed across 3 funnel stages
- 70% activation rate (signed_up → sent_message)
- 30% revenue conversion rate (signed_up → upgraded_to_pro)
- Biggest actionable drop-off: activation → revenue, not top of funnel

## Recommendation
Investigate session depth differences between users who converted 
to Pro vs those who activated but didn't convert. Hypothesis: 
converters had longer first sessions.

## Resume Bullet
Analyzed 10-user onboarding funnel revealing 70% activation rate 
and 30% revenue conversion rate using SQL, identifying 
activation-to-revenue drop-off as the primary growth opportunity.