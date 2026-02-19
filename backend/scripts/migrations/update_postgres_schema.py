import psycopg2
from urllib.parse import urlparse
import os

# Parse DATABASE_URL from .env manually or hardcode based on view_file output
# DATABASE_URL=postgresql://postgres.emyjtnrxuweihgramybf:ibOs.ko321po@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
DB_URL = "postgresql://postgres.emyjtnrxuweihgramybf:ibOs.ko321po@aws-1-eu-central-1.pooler.supabase.com:6543/postgres"

def migrate_db():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("Connected to Postgres...")

        # 1. Add columns to customers
        try:
            print("Adding engagement_score to customers...")
            cur.execute("ALTER TABLE customers ADD COLUMN IF NOT EXISTS engagement_score FLOAT DEFAULT 1.0;")
            conn.commit()
        except Exception as e:
            print(f"Error adding engagement_score: {e}")
            conn.rollback()

        try:
            print("Adding interested_in_marketing to customers...")
            cur.execute("ALTER TABLE customers ADD COLUMN IF NOT EXISTS interested_in_marketing BOOLEAN DEFAULT FALSE;")
            conn.commit()
        except Exception as e:
            print(f"Error adding interested_in_marketing: {e}")
            conn.rollback()

        # 2. Create coupons table
        print("Creating coupons table...")
        create_coupons_sql = """
        CREATE TABLE IF NOT EXISTS coupons (
            id SERIAL PRIMARY KEY,
            code VARCHAR(255) UNIQUE,
            customer_id INTEGER REFERENCES customers(id),
            store_id INTEGER REFERENCES stores(id),
            discount_amount FLOAT,
            discount_type VARCHAR(50) DEFAULT 'PERCENT',
            is_used BOOLEAN DEFAULT FALSE,
            valid_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            cur.execute(create_coupons_sql)
            conn.commit()
            print("Coupons table created.")
        except Exception as e:
            print(f"Error creating coupons table: {e}")
            conn.rollback()

        cur.close()
        conn.close()
        print("Migration complete.")

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    migrate_db()
