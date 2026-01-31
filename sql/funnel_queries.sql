-- Funnel stage counts (unique users per stage)
SELECT
    event_name,
    COUNT(DISTINCT user_id) AS users
FROM events
WHERE event_name IN (
    'visit',
    'sign_up',
    'kyc_start',
    'kyc_approved',
    'first_deposit',
    'first_trade',
    'retained_7d'
)
GROUP BY event_name
ORDER BY CASE event_name
    WHEN 'visit' THEN 1
    WHEN 'sign_up' THEN 2
    WHEN 'kyc_start' THEN 3
    WHEN 'kyc_approved' THEN 4
    WHEN 'first_deposit' THEN 5
    WHEN 'first_trade' THEN 6
    WHEN 'retained_7d' THEN 7
END;
