-- ============================
-- TASK 6: FEATURE ENGINEERING
-- ============================

-- 1. USER-LEVEL FEATURES
CREATE TABLE IF NOT EXISTS user_features (
    user_id BIGINT PRIMARY KEY,
    activity_count INTEGER,
    avg_price NUMERIC(10,2)
);

INSERT INTO user_features
SELECT
    user_id,
    COUNT(*) AS activity_count,
    AVG(price) AS avg_price
FROM ecommerce_events
GROUP BY user_id
ON CONFLICT (user_id)
DO UPDATE SET
    activity_count = EXCLUDED.activity_count,
    avg_price = EXCLUDED.avg_price;


-- 2. ITEM-LEVEL FEATURES
CREATE TABLE IF NOT EXISTS item_features (
    product_id BIGINT PRIMARY KEY,
    interaction_count INTEGER,
    avg_price NUMERIC(10,2)
);

INSERT INTO item_features
SELECT
    product_id,
    COUNT(*) AS interaction_count,
    AVG(price) AS avg_price
FROM ecommerce_events
GROUP BY product_id
ON CONFLICT (product_id)
DO UPDATE SET
    interaction_count = EXCLUDED.interaction_count,
    avg_price = EXCLUDED.avg_price;


-- 3. USER-ITEM INTERACTION FEATURES
CREATE TABLE IF NOT EXISTS user_item_features (
    user_id BIGINT,
    product_id BIGINT,
    interaction_count INTEGER,
    PRIMARY KEY (user_id, product_id)
);

INSERT INTO user_item_features
SELECT
    user_id,
    product_id,
    COUNT(*) AS interaction_count
FROM ecommerce_events
GROUP BY user_id, product_id
ON CONFLICT (user_id, product_id)
DO UPDATE SET
    interaction_count = EXCLUDED.interaction_count;
