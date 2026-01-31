WITH stage_counts AS (
    SELECT 'visit' AS stage, COUNT(DISTINCT user_id) AS users
    FROM events WHERE event_name = 'visit'
    UNION ALL
    SELECT 'sign_up', COUNT(DISTINCT user_id)
    FROM events WHERE event_name = 'sign_up'
    UNION ALL
    SELECT 'kyc_start', COUNT(DISTINCT user_id)
    FROM events WHERE event_name = 'kyc_start'
    UNION ALL
    SELECT 'kyc_approved', COUNT(DISTINCT user_id)
    FROM events WHERE event_name = 'kyc_approved'
    UNION ALL
    SELECT 'first_deposit', COUNT(DISTINCT user_id)
    FROM events WHERE event_name = 'first_deposit'
    UNION ALL
    SELECT 'first_trade', COUNT(DISTINCT user_id)
    FROM events WHERE event_name = 'first_trade'
    UNION ALL
    SELECT 'retained_7d', COUNT(DISTINCT user_id)
    FROM events WHERE event_name = 'retained_7d'
),
ordered AS (
    SELECT
        stage,
        users,
        CASE stage
            WHEN 'visit' THEN 1
            WHEN 'sign_up' THEN 2
            WHEN 'kyc_start' THEN 3
            WHEN 'kyc_approved' THEN 4
            WHEN 'first_deposit' THEN 5
            WHEN 'first_trade' THEN 6
            WHEN 'retained_7d' THEN 7
        END AS step
    FROM stage_counts
),
with_prev AS (
    SELECT
        stage,
        users,
        step,
        LAG(users) OVER (ORDER BY step) AS prev_users
    FROM ordered
)
SELECT
    stage,
    users,
    ROUND(1.0 * users / (SELECT users FROM ordered WHERE step = 1), 4) AS overall_conv_from_visit,
    ROUND(1.0 * users / prev_users, 4) AS step_conv_from_prev,
    ROUND(1.0 - (1.0 * users / prev_users), 4) AS step_dropoff
FROM with_prev
ORDER BY step;
