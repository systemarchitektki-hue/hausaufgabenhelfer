-- Hausaufgabenhelfer Pro - Supabase Schema
-- Führe dieses SQL in deinem Supabase Dashboard aus (SQL Editor)

-- Tabelle für Zugangscodes
CREATE TABLE IF NOT EXISTS access_codes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE,
    last_used TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    notes TEXT
);

-- Index für schnelle Code-Suche
CREATE INDEX IF NOT EXISTS idx_access_codes_code ON access_codes(code);
CREATE INDEX IF NOT EXISTS idx_access_codes_active ON access_codes(is_active);

-- Beispiel-Codes einfügen (optional - zum Testen)
INSERT INTO access_codes (code, name, notes) VALUES 
    ('TEST-123-ABC', 'Test Benutzer', 'Zum Testen der App'),
    ('DEMO-456-XYZ', 'Demo Account', 'Demo-Zugang')
ON CONFLICT (code) DO NOTHING;

-- Row Level Security aktivieren
ALTER TABLE access_codes ENABLE ROW LEVEL SECURITY;

-- Policy: Nur authentifizierte Benutzer können lesen
CREATE POLICY "Allow anon read" ON access_codes
    FOR SELECT USING (true);

-- Policy: Nur Service-Role kann schreiben
CREATE POLICY "Allow service write" ON access_codes
    FOR ALL USING (auth.role() = 'service_role');
