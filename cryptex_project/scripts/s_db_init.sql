-- Creates the table to store all found signals
CREATE TABLE IF NOT EXISTS public.trading_signals (
    id SERIAL PRIMARY KEY,
    signal_id VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    trader_id VARCHAR(255),
    exchange VARCHAR(100),
    asset VARCHAR(50),
    direction VARCHAR(10),
    trade_size_usd NUMERIC,
    leverage NUMERIC,
    catalyst_source VARCHAR(100),
    catalyst_headline TEXT,
    time_delta_minutes INT,
    ai_confidence_score INT,
    status VARCHAR(50) DEFAULT 'NEW'
);

-- Creates tables for our listeners to store recent events for correlation
CREATE TABLE IF NOT EXISTS public.recent_trades (
    id SERIAL PRIMARY KEY,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    trader_id VARCHAR(255),
    asset VARCHAR(50),
    raw_data JSONB
);

CREATE TABLE IF NOT EXISTS public.recent_catalysts (
    id SERIAL PRIMARY KEY,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    headline TEXT,
    source VARCHAR(100),
    asset_tags TEXT[],
    raw_data JSONB
);

-- Prune old events to keep tables small and fast
CREATE INDEX IF NOT EXISTS idx_recent_trades_time ON public.recent_trades(ingested_at);
CREATE INDEX IF NOT EXISTS idx_recent_catalysts_time ON public.recent_catalysts(ingested_at);
DELETE FROM recent_trades WHERE ingested_at < NOW() - INTERVAL '1 hour';
DELETE FROM recent_catalysts WHERE ingested_at < NOW() - INTERVAL '1 hour';