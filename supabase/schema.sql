-- Luxury Furniture Studio - Supabase Schema
-- Run this in your Supabase SQL Editor after creating a new project

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- PROFILES TABLE (extends auth.users)
-- ============================================
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    email TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    avatar_url TEXT,
    phone TEXT,
    address JSONB DEFAULT '{}'::jsonb
);

-- RLS for profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.profiles FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
    ON public.profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, first_name, last_name)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'first_name',
        NEW.raw_user_meta_data->>'last_name'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- FURNITURE TABLE
-- ============================================
CREATE TABLE public.furniture (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    materials TEXT[] DEFAULT '{}',
    dimensions JSONB DEFAULT '{"width": 0, "depth": 0, "height": 0}'::jsonb,
    colors TEXT[] DEFAULT '{}',
    features TEXT[] DEFAULT '{}',
    image_url TEXT,
    model_path TEXT,
    is_featured BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true
);

-- Public read access for furniture catalog
ALTER TABLE public.furniture ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view furniture"
    ON public.furniture FOR SELECT
    TO authenticated, anon
    USING (true);

-- Index for common queries
CREATE INDEX idx_furniture_category ON public.furniture(category);
CREATE INDEX idx_furniture_featured ON public.furniture(is_featured) WHERE is_featured = true;

-- ============================================
-- USER FAVORITES TABLE
-- ============================================
CREATE TABLE public.favorites (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    furniture_id UUID REFERENCES public.furniture(id) ON DELETE CASCADE NOT NULL,
    UNIQUE(user_id, furniture_id)
);

ALTER TABLE public.favorites ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own favorites"
    ON public.favorites FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can add favorites"
    ON public.favorites FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove favorites"
    ON public.favorites FOR DELETE
    USING (auth.uid() = user_id);

CREATE INDEX idx_favorites_user ON public.favorites(user_id);

-- ============================================
-- CUSTOM DESIGN REQUESTS TABLE
-- ============================================
CREATE TABLE public.design_requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    furniture_type TEXT NOT NULL,
    description TEXT NOT NULL,
    preferred_materials TEXT[],
    dimensions JSONB,
    budget_range TEXT,
    timeline TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'reviewing', 'quoted', 'approved', 'in_progress', 'completed', 'cancelled')),
    notes TEXT
);

ALTER TABLE public.design_requests ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own design requests"
    ON public.design_requests FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create design requests"
    ON public.design_requests FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own design requests"
    ON public.design_requests FOR UPDATE
    USING (auth.uid() = user_id);

CREATE INDEX idx_design_requests_user ON public.design_requests(user_id);
CREATE INDEX idx_design_requests_status ON public.design_requests(status);

-- ============================================
-- CONSULTATION BOOKINGS TABLE
-- ============================================
CREATE TABLE public.consultations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    consultation_type TEXT NOT NULL CHECK (consultation_type IN ('virtual', 'in_person', 'home_visit')),
    location TEXT,
    notes TEXT,
    status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'completed', 'cancelled'))
);

ALTER TABLE public.consultations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own consultations"
    ON public.consultations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can book consultations"
    ON public.consultations FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own consultations"
    ON public.consultations FOR UPDATE
    USING (auth.uid() = user_id);

CREATE INDEX idx_consultations_user ON public.consultations(user_id);
CREATE INDEX idx_consultations_scheduled ON public.consultations(scheduled_at);

-- ============================================
-- AI CHAT HISTORY (for Claude integration)
-- ============================================
CREATE TABLE public.chat_history (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    session_id UUID NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own chat history"
    ON public.chat_history FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert chat messages"
    ON public.chat_history FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE INDEX idx_chat_history_user ON public.chat_history(user_id);
CREATE INDEX idx_chat_history_session ON public.chat_history(session_id);

-- ============================================
-- SEED DATA - Initial Furniture Catalog
-- ============================================
INSERT INTO public.furniture (name, category, description, price, materials, dimensions, colors, features, image_url, model_path, is_featured) VALUES
(
    'Milano Sofa',
    'Seating',
    'Handcrafted Italian leather sofa with walnut frame and brass accents. Each piece is meticulously crafted by our artisans in Italy, using the finest full-grain leather and sustainable walnut.',
    8950.00,
    ARRAY['Leather', 'Walnut', 'Brass'],
    '{"width": 220, "depth": 95, "height": 85}'::jsonb,
    ARRAY['#8B4513', '#694A38', '#241C1C', '#A67D5D', '#D8C4B8'],
    ARRAY['Premium Down Cushions', 'Brass Hardware', 'Hand-Stitched Detailing'],
    '/assets/furniture/sofa.jpg',
    '/assets/models/milano_sofa.glb',
    true
),
(
    'Vienna Coffee Table',
    'Tables',
    'Exquisite Calacatta marble top coffee table with a sculpted bronze base. The veining in each marble slab is unique, carefully selected from the finest quarries in Italy.',
    5650.00,
    ARRAY['Marble', 'Bronze'],
    '{"width": 120, "depth": 80, "height": 45}'::jsonb,
    ARRAY['#FFFFFF', '#F5F5F5', '#D4C4A8', '#D4AC0D', '#614E13'],
    ARRAY['Book-Matched Marble', 'Acid-Etched Bronze', 'Felt-Lined Base'],
    '/assets/furniture/coffee_table.jpg',
    '/assets/models/vienna_coffee_table.glb',
    true
),
(
    'Oslo Dining Chair',
    'Seating',
    'Scandinavian-inspired dining chair with woven leather seat and solid oak frame. The minimalist design emphasizes clean lines and natural materials.',
    2450.00,
    ARRAY['Oak', 'Leather'],
    '{"width": 50, "depth": 55, "height": 80}'::jsonb,
    ARRAY['#A1887F', '#5D4037', '#D7CCC8', '#796A62', '#382E2C'],
    ARRAY['Hand-Woven Seat', 'Mortise and Tenon Joinery', 'Oil-Rubbed Finish'],
    '/assets/furniture/chair.jpg',
    '/assets/models/oslo_dining_chair.glb',
    false
),
(
    'Manhattan Bookshelf',
    'Storage',
    'Modular bookshelf system with adjustable shelves and integrated LED lighting. Features hidden cable management and smart lighting.',
    11200.00,
    ARRAY['Walnut', 'Glass', 'Brass'],
    '{"width": 180, "depth": 45, "height": 240}'::jsonb,
    ARRAY['#5D4037', '#3E2723', '#8D6E63', '#D4AC0D', '#212121'],
    ARRAY['Integrated Lighting', 'Smart Home Compatible', 'Adjustable Shelving', 'Cable Management'],
    '/assets/furniture/bookshelf.jpg',
    '/assets/models/manhattan_bookshelf.glb',
    true
),
(
    'Kyoto Side Table',
    'Tables',
    'Japanese-inspired side table with intricate woodwork and a hidden compartment. Features hand-cut joinery and shou sugi ban accent details.',
    3950.00,
    ARRAY['Cherry Wood', 'Maple'],
    '{"width": 60, "depth": 60, "height": 55}'::jsonb,
    ARRAY['#C37B57', '#92603B', '#4A3829', '#7D4E24', '#D69967'],
    ARRAY['Hidden Compartment', 'Hand-Cut Joinery', 'Shou Sugi Ban Accents'],
    '/assets/furniture/side_table.jpg',
    '/assets/models/kyoto_side_table.glb',
    false
),
(
    'Paris Pendant Light',
    'Lighting',
    'Hand-blown glass pendant with brushed brass fittings. Each pendant is uniquely created by master glassblowers with subtle variations.',
    4250.00,
    ARRAY['Glass', 'Brass'],
    '{"width": 45, "depth": 45, "height": 60}'::jsonb,
    ARRAY['#F0F0F0', '#E0E0E0', '#D4AC0D', '#CFD8DC', '#BDBDBD'],
    ARRAY['Dimmable LED', 'Hand-Blown Glass', 'Adjustable Height'],
    '/assets/furniture/pendant.jpg',
    '/assets/models/paris_pendant.glb',
    true
);
