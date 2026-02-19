-- BU SCRIPT SUPABASE SQL EDITOR ÜZERİNDE ÇALIŞTIRILMALIDIR

-- 1. Pgcrypto eklentisinin açık olduğundan emin ol (Şifreleme için gerekli)
create extension if not exists "pgcrypto";

-- 2. Kullanıcıları oluştur (user1 - user10)
-- Şifre: '123456' (Kendi istediğiniz şifreyi '123456' yerine yazabilirsiniz)
-- Email onayını (email_confirmed_at) dolu gönderiyoruz ki direkt giriş yapabilsinler.

DO $$
DECLARE
  i integer;
  new_user_id uuid;
  user_email text;
  user_password text := '123456'; -- Tüm kullanıcılar için ortak şifre
BEGIN
  FOR i IN 1..10 LOOP
    user_email := 'user' || i || '@retaildss.com';
    
    -- Eğer kullanıcı zaten yoksa ekle
    IF NOT EXISTS (SELECT 1 FROM auth.users WHERE email = user_email) THEN
      
      INSERT INTO auth.users (
        instance_id,
        id,
        aud,
        role,
        email,
        encrypted_password,
        email_confirmed_at,
        recovery_sent_at,
        last_sign_in_at,
        raw_app_meta_data,
        raw_user_meta_data,
        created_at,
        updated_at,
        confirmation_token,
        email_change,
        email_change_token_new,
        recovery_token
      ) VALUES (
        '00000000-0000-0000-0000-000000000000', -- Default instance_id
        gen_random_uuid(),
        'authenticated',
        'authenticated',
        user_email,
        crypt(user_password, gen_salt('bf')), -- Şifreyi hashle
        now(), -- Email onaylanmış say
        now(),
        now(),
        '{"provider":"email","providers":["email"]}',
        json_build_object('username', 'user' || i), -- Username meta dataya ekle
        now(),
        now(),
        '',
        '',
        '',
        ''
      );
      
      RAISE NOTICE 'Kullanıcı oluşturuldu: %', user_email;
      
    ELSE
      RAISE NOTICE 'Kullanıcı zaten var: %', user_email;
    END IF;
  END LOOP;
END $$;
