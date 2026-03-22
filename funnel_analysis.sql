-- funnel analysis: number of users drop off at each stage
SELECT event_name, COUNT(DISTINCT uesr_id) AS user_count
FROM user_events
WHERE event_name IN ('signed_up', 'sent_message', 'upgraded_to_pro')
GROUP BY event_name;

-- Users who never sent a message

-- Event sequence for each user