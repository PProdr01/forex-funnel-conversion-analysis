WITH funnel AS (
    SELECT
        channel,
        COUNT(DISTINCT CASE WHEN event_name = 'visit' THEN user_id END) AS visit_users,
        COUNT(DISTINCT CASE WHEN event_name = 'sign_up' THEN user_id END) AS signup_users,
        COUNT(DISTINCT CASE WHEN event_name = 'kyc_approved' THEN user_id END) AS kyc_approved_users,
        COUNT(DISTINCT CASE WHEN event_name = 'first_deposit' THEN user_id END) AS deposit_users,
        COUNT(DISTINCT CASE WHEN event_name = 'first_trade' THEN user_id END) AS trade_users,
        COUNT(DISTINCT CASE WHEN event_name = 'retained_7d' THEN user_id END) AS retained_users
    FROM events
    GROUP BY channel
)
SELECT
    channel,
    visit_users,
    signup_users,
    ROUND(1.0 * signup_users / visit_users, 4) AS visit_to_signup,
    kyc_approved_users,
    ROUND(1.0 * kyc_approved_users / signup_users, 4) AS signup_to_kyc_approved,
    deposit_users,
    ROUND(1.0 * deposit_users / kyc_approved_users, 4) AS kyc_to_deposit,
    trade_users,
    ROUND(1.0 * trade_users / deposit_users, 4) AS deposit_to_trade,
    retained_users,
    ROUND(1.0 * retained_users / trade_users, 4) AS trade_to_retained_7d
FROM funnel
ORDER BY trade_users DESC;
