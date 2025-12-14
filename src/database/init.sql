-- 1. Tabela Konfiguracji Bota (Single Source of Truth)
-- Tu trzymamy ustawienia zamiast w kodzie (Hardcode Killer)
CREATE TABLE IF NOT EXISTS bot_config (
    key VARCHAR(50) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Przykładowy wsad startowy (Język i Prefix)
INSERT INTO bot_config (key, value, description) VALUES 
('language', '"pl"', 'Domyślny język bota (pl/en)'),
('maintenance_mode', 'false', 'Czy bot jest w trybie prac technicznych?');


-- 2. Tabela Klanów (Możemy obsługiwać jeden, lub wiele w przyszłości)
CREATE TABLE IF NOT EXISTS clans (
    tag VARCHAR(15) PRIMARY KEY,
    name VARCHAR(50),
    server_id BIGINT NOT NULL, -- ID serwera Discord
    log_channel_id BIGINT,     -- Gdzie wysyłać logi
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 3. Tabela Graczy (Historia)
CREATE TABLE IF NOT EXISTS players (
    tag VARCHAR(15) PRIMARY KEY,
    name VARCHAR(50),
    discord_id BIGINT, -- Połączenie z Discordem
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 4. Tabela Logów (AUDIT LOG - To o co pytałeś)
-- Typ wyliczeniowy dla porządku
CREATE TYPE log_event_type AS ENUM ('ROLE_CHANGE', 'WAR_UPDATE', 'MEMBER_FLOW', 'SETTINGS_CHANGE');

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    clan_tag VARCHAR(15) REFERENCES clans(tag),
    event_type log_event_type NOT NULL,
    severity VARCHAR(10) DEFAULT 'INFO', -- INFO, WARN, CRITICAL
    
    -- MAGIA JSONB: Tu zapisujemy szczegóły zdarzenia
    -- Dla awansu: {"player": "Nick", "old": "member", "new": "elder", "by": "admin_tag"}
    -- Dla wojny: {"enemy": "EnemyClan", "stars": 3}
    details JSONB NOT NULL, 
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indeks dla szybkiego wyszukiwania logów po dacie i typie (Wydajność)
CREATE INDEX idx_audit_logs_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_date ON audit_logs(created_at);