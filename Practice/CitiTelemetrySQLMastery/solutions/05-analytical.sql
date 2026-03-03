-- =============================================================================
-- 05 — ANALYTICAL PATTERNS — SOLUTIONS
-- =============================================================================

-- 3. Funnel conversion rates
WITH steps AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_type = 'view'        THEN 1 END) AS saw_view,
        MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 END) AS saw_cart,
        MAX(CASE WHEN event_type = 'checkout'    THEN 1 END) AS saw_checkout,
        MAX(CASE WHEN event_type = 'purchase'    THEN 1 END) AS saw_purchase
    FROM user_events
    GROUP BY user_id
)
SELECT 
    COUNT(*) AS total_users,
    COUNT(CASE WHEN saw_view = 1 THEN 1 END) AS viewed,
    COUNT(CASE WHEN saw_cart = 1 THEN 1 END) AS added_to_cart,
    COUNT(CASE WHEN saw_checkout = 1 THEN 1 END) AS checkout,
    COUNT(CASE WHEN saw_purchase = 1 THEN 1 END) AS purchased,
    ROUND(100.0 * COUNT(CASE WHEN saw_cart = 1 THEN 1 END)     / NULLIF(COUNT(CASE WHEN saw_view = 1 THEN 1 END), 0), 1) AS view_to_cart_pct,
    ROUND(100.0 * COUNT(CASE WHEN saw_purchase = 1 THEN 1 END) / NULLIF(COUNT(CASE WHEN saw_view = 1 THEN 1 END), 0), 1) AS view_to_buy_pct
FROM steps;

-- 4. 7-day rolling average (example for last few days)
SELECT 
    server_id,
    collection_date,
    cpu_utilization,
    ROUND(AVG(cpu_utilization) OVER (
        PARTITION BY server_id 
        ORDER BY collection_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 1) AS roll_avg_7d
FROM telemetry
WHERE collection_date >= '2026-01-08'
ORDER BY server_id, collection_date;
