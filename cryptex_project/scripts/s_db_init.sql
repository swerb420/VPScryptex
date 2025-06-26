-- Drop table if it exists to ensure a clean slate with the new schema
DROP TABLE IF EXISTS public.trading_signals;

-- Re-create the table with new fields for advanced analysis
CREATE TABLE IF NOT EXISTS public.trading_signals (
    id SERIAL PRIMARY KEY,
    signal_id VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    trader_id VARCHAR(255),
    exchange VARCHAR(100),
    asset VARCHAR(50),
    direction VARCHAR(10),
    trade_size_usd NUMERIC,

    -- New Intelligence Fields
    catalyst_headline TEXT,
    legitimacy_score INT, -- (0-100) How real is the news?
    herd_index INT,       -- (0-100) How many other smart wallets are doing this?
    historical_win_rate INT, -- (0-100) How often has this pattern worked before?
    safety_rating VARCHAR(50), -- 'SAFE', 'CAUTION', 'DANGER'

    -- Final AI Verdict
    ai_confidence_score INT,
    ai_summary TEXT,
    status VARCHAR(50) DEFAULT 'NEW'
);

-- The other tables remain the same...
CREATE TABLE IF NOT EXISTS public.recent_trades (id SERIAL PRIMARY KEY, ingested_at TIMESTAMPTZ DEFAULT NOW(), trader_id VARCHAR(255), asset VARCHAR(50), raw_data JSONB);
CREATE TABLE IF NOT EXISTS public.recent_catalysts (id SERIAL PRIMARY KEY, ingested_at TIMESTAMPTZ DEFAULT NOW(), headline TEXT, source VARCHAR(100), asset_tags TEXT[], raw_data JSONB);
CREATE TABLE IF NOT EXISTS public.monitored_traders (id SERIAL PRIMARY KEY, identifier VARCHAR(255) NOT NULL UNIQUE, exchange VARCHAR(100) NOT NULL, description TEXT, is_active BOOLEAN DEFAULT TRUE);
INSERT INTO public.monitored_traders (identifier, exchange, description, is_active) VALUES ('4258234B3958932C2556734194539825', 'Binance Futures', 'Example Top Trader ID', TRUE) ON CONFLICT (identifier) DO NOTHING;