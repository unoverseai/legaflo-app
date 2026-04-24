-- 1. ENUMS
CREATE TYPE user_role AS ENUM ('citizen', 'advocate', 'firm_admin', 'firm_member');
CREATE TYPE doc_category AS ENUM ('fir', 'order', 'draft', 'evidence_media', 'vault_private', 'invoice');
CREATE TYPE case_status AS ENUM ('active', 'disposed', 'stayed', 'appeal');

-- 2. USERS, FIRMS & ADVOCATE NETWORK
CREATE TABLE firms (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  gstin TEXT UNIQUE,
  subscription_tier TEXT CHECK (subscription_tier IN ('Starter', 'Pro', 'Enterprise')),
  workspace_settings JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT NOT NULL,
  role user_role NOT NULL,
  bar_council_id TEXT UNIQUE,
  jurisdiction_courts TEXT[], 
  firm_id UUID REFERENCES firms(id) ON DELETE SET NULL,
  phone TEXT UNIQUE,
  telegram_chat_id TEXT,
  preferred_language TEXT DEFAULT 'en',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. CASE MANAGEMENT & CNR TRACKING
CREATE TABLE cases (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  cnr_number TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  court_name TEXT,
  judge_name TEXT,
  status case_status DEFAULT 'active',
  next_hearing_date DATE,
  client_id UUID REFERENCES profiles(id),
  lead_advocate_id UUID REFERENCES profiles(id),
  firm_id UUID REFERENCES firms(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. DIGITAL VAULT & EVIDENCE (BSA Sec 63 Compliant)
CREATE TABLE documents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
  uploaded_by UUID REFERENCES profiles(id),
  file_url TEXT NOT NULL, 
  category doc_category NOT NULL,
  sha256_hash TEXT NOT NULL, -- Mandatory for Section 63(4) Evidence Act
  is_sgi_tagged BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. INVOICING & PAYMENTS
CREATE TABLE invoices (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  advocate_id UUID REFERENCES profiles(id),
  client_id UUID REFERENCES profiles(id),
  amount NUMERIC NOT NULL,
  payment_link TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. AUDIT LOGS (Immutable)
CREATE TABLE audit_logs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id),
  action TEXT NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT now()
);

-- ==========================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==========================================
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy 1: Citizens can only see their own docs
CREATE POLICY "Citizen Vault Access" ON documents FOR SELECT
USING (auth.uid() = uploaded_by AND (SELECT role FROM profiles WHERE id = auth.uid()) = 'citizen');

-- Policy 2: Firm members share access to firm cases
CREATE POLICY "Firm Workspace Access" ON documents FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM cases c
    JOIN profiles p ON c.firm_id = p.firm_id
    WHERE c.id = documents.case_id AND p.id = auth.uid()
  )
);
