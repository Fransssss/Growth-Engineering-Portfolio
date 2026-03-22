-- Funnel analysis: number of users drop off at each stage
SELECT event_name, COUNT(DISTINCT user_id) AS user_count
FROM user_events
WHERE event_name IN ('signed_up', 'sent_message', 'upgraded_to_pro')
GROUP BY event_name;

-- Users who never sent a message
SELECT u.name, e.event_name,
FROM users u
LEFT JOIN user_events e 
ON u.user_id = e.user_id 
WHERE e.event_name is NULL;

-- Event sequence for each user
SELECT user_id, event_name, created_at,
ROW_NUMBER() OVER (PARTITION BY user_id 
ORDER BY created_at)
AS event_order
FROM user_events;