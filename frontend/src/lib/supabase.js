
import { createClient } from '@supabase/supabase-js';

// .env dosyasından Supabase URL ve Key alınıyor
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

// Hata ayıklama için konsola log (Canlı ortamda kaldırılabilir)
if (!supabaseUrl || !supabaseAnonKey) {
    console.warn('Supabase URL veya Anon Key eksik! Lütfen .env dosyasını kontrol edin.');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
