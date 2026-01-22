-- ======================================
-- FEATURE STORE: FEATURE REGISTRY
-- ======================================

CREATE TABLE IF NOT EXISTS feature_registry (
    feature_name TEXT PRIMARY KEY,
    source_table TEXT,
    transformation_logic TEXT,
    feature_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
