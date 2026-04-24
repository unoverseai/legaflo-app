# 🚀 Master PRD: LegaFlo Legal Operating System (2026 Edition)

## 1. Executive Summary & Vision
**LegaFlo** is an end-to-end Legal Operating System designed for the Indian legal ecosystem. Moving beyond reactive chatbots, LegaFlo utilizes **Agentic AI** to proactively manage cases, draft court-ready documents, predict legal outcomes, and secure digital evidence. 

**Core Objective:** To bridge the gap between Citizens, Advocates, and Law Firms through a unified, zero-hallucination, legally compliant platform (adhering strictly to BNS and BSA 2023 standards).

---

## 2. The Dashboard Ecosystem (Features & Workflows)

### A. Citizen Dashboard (Public Legal Self-Help)
* **AI Document Translation:** Translates complex legal documents (FIRs, Notices) into 15+ regional Indian languages.
* **AI Plain-Language Case Summaries:** Converts dense court orders into simple summaries with identified risks.
* **Draft Official Letter:** AI-generation of formal correspondence (RTIs, Consumer Grievances, Tenant-Landlord Notices) with mandatory 2026 SGI (Synthetic Generation) tagging.
* **Consumer Court Help:** Specialized guided workflows for drafting and filing grievances in Indian Consumer Forums.
* **Find an Advocate (Court-wise):** A directory/matchmaking algorithm connecting citizens to the right lawyer based on jurisdiction and case type.
* **Case Tracking & Hearing Alerts:** Real-time CNR syncing with automated Telegram alerts for hearing dates.

### B. Advocate Dashboard (Solo Practice Command Center)
* **AI Lawyer Chat:** 24/7 instant legal opinions, case strategies, and procedural guidance.
* **AI Court-Ready Drafting:** Generates petitions, replies, and notices using strict Indian legal formatting.
* **AI Order Analysis:** Upload any court order for instant summaries, key findings, and recommended next steps.
* **AI Law Search Engine:** Rapid search across Indian Acts and Bare Laws with AI-curated case citations.
* **Digital Vault & Security:** Bank-grade encrypted storage for case files and sensitive client data.
* **Invoicing & Payments:** Automated professional invoices with tax calculations and Razorpay payment links.
* **Telegram Alerts:** Automated reminders for deadlines, court appearances, and pending client payments.
* **Verdict Predictor:** Judge-specific analytics predicting outcomes based on historical High Court data.
* **Digital Witness (Evidence Formatter):** Automatically processes digital evidence and generates the mandatory **Section 63(4) BSA Certificate** with SHA-256 hashes.

### C. Law Firm Dashboard (Enterprise Workspace)
* **Team Workspace:** Collaboration tools for case assignment, task tracking, and shared document access.
* **Centralized Billing:** Master control over the firm's finances and multi-advocate invoicing.
* **Conflict of Interest Check:** Auto-scans new client data against the firm’s entire historical database to prevent ethical breaches.
* **Agentic Proactive Workflows:** AI agents that monitor cases and automatically draft routine filings (e.g., "Application for Certified Copy") the moment an order is passed.

### D. System-Wide "Killer" Features
* **The "Mercy-Check" Engine:** A hallucination-prevention layer that verifies every generated legal citation against the official **Digital SCR** before it reaches the user.
* **Prop-Check:** Automated real estate due diligence integrating with DILRMP/ULPIN to trace the 20-year chain of title.

---

## 3. Complete Database Schema (Supabase/Postgres)
*Note: This schema utilizes strict Row Level Security (RLS) to ensure enterprise-grade multi-tenant isolation.*

```sql
-- 1. ENUMS
CREATE TYPE user_role AS ENUM ('citizen', 'advocate', 'firm_admin', 'firm_member');
CREATE TYPE doc_category AS ENUM ('fir', 'order', 'draft', 'evidence_media', 'vault_private', 'invoice');
CREATE TYPE case_status AS ENUM ('active', 'disposed', 'stayed', 'appeal');

-- 2. USERS, FIRMS & ADVOCATE NETWORK
CREATE TABLE firms (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  gstin TEXT UNIQUE,
  subscription_tier TEXT CHECK (tier IN ('Starter', 'Pro', 'Enterprise')),
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

-----------------


4. Technical Architecture & Integrations
A. Frontend (User Interface)
Framework: Next.js 15 (App Router) for Server-Side Rendering (vital for SEO on "Find an Advocate").

State Management: Zustand (lightweight, perfect for real-time CNR updates).

Styling: Tailwind CSS v4 + shadcn/ui.

B. Backend (Agentic Orchestration)
Primary API: FastAPI (Python 3.12).

AI Framework: LangGraph (manages the reasoning loops and multi-agent coordination).

Database Client: Supabase Edge Functions (TypeScript) for CRUD, Auth, and Webhooks.

C. Core Integrations
Payments: Razorpay API (Invoicing & Subscriptions).

Notifications: Telegram Bot API (Automated hearing/payment alerts).

Legal Data: Digital SCR API (for Mercy-Check), e-Courts API (for CNR tracking).

5. Development Pipeline & CI/CD
To ensure a stable structure with minimum code breaks, LegaFlo utilizes a Maker-Checker Pipeline.

Architecture Definition (Cursor IDE): Lead Architect establishes Supabase Types, API routing, and .env configs.

Autonomous Feature Building (Antigravity): Agent builds modules based on this PRD and .antigravityrules.

The "Checker" (CodeRabbit AI): Intercepts PRs to scan for:

RLS bypass attempts.

Missing SHA-256 hashes (BSA compliance).

Missing "Mercy-Check" hallucination guards.

Auto-rectifies and commits fixes before merging.

6. Development Roadmap
Phase 1: Foundation (Weeks 1-3)

Deploy Supabase schema, Auth, and Digital Vault.

Build Next.js UI shells for all three dashboards.

Phase 2: Core Legal AI (Weeks 4-6)

Integrate FastAPI & LangGraph.

Develop "Draft Official Letter", AI Translation, and AI Order Analysis.

Implement the "Mercy-Check" citation loop.

Phase 3: The "Killer" Features (Weeks 7-10)

Build Verdict Predictor using historical data.

Implement Digital Witness (Section 63 PDF generator).

Connect Telegram API for alerts.

Phase 4: Enterprise & Launch (Weeks 11-12)

Finalize Firm Workspace (Role-based access, shared billing).

Integrate Razorpay.

Perform OWASP security audit.