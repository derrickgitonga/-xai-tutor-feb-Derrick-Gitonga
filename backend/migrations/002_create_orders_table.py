"""
Migration: Create orders table
Version: 002
Description: Creates the orders table with all required columns and seeds mock data
"""

import sqlite3
import sys
import os
import uuid
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import DATABASE_PATH


def upgrade():
    """Apply the migration."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create migrations tracking table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check if this migration has already been applied
    cursor.execute("SELECT 1 FROM _migrations WHERE name = ?", ("002_create_orders_table",))
    if cursor.fetchone():
        print("Migration 002_create_orders_table already applied. Skipping.")
        conn.close()
        return

    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            order_number TEXT NOT NULL UNIQUE,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_avatar TEXT,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'completed', 'refunded')),
            total_amount REAL NOT NULL,
            payment_status TEXT NOT NULL CHECK(payment_status IN ('paid', 'unpaid')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Seed mock data matching the design
    # Status options: 'pending', 'completed', 'refunded'
    # Payment status options: 'paid', 'unpaid'
    # Avatar colors for variety
    colors = ["f97316", "3b82f6", "10b981", "8b5cf6", "ec4899", "06b6d4", "f59e0b", "ef4444", "6366f1", "14b8a6"]

    def avatar_url(name, color):
        """Generate UI Avatars URL for a customer name."""
        formatted_name = name.replace(" ", "+")
        return f"https://ui-avatars.com/api/?name={formatted_name}&background={color}&color=fff&size=40&bold=true"

    now = datetime.utcnow().isoformat()
    mock_orders = [
        # Recent orders (January 2025)
        (str(uuid.uuid4()), "#ORD1050", "Esther Kiehn", "esther@example.com", avatar_url("Esther Kiehn", colors[0]), "2025-01-31", "pending", 10.50, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1049", "Denise Kuhn", "denise@example.com", avatar_url("Denise Kuhn", colors[1]), "2025-01-30", "pending", 100.50, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1048", "Clint Hoppe", "clint@example.com", avatar_url("Clint Hoppe", colors[2]), "2025-01-30", "completed", 60.56, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1047", "Darin Deckow", "darin@example.com", avatar_url("Darin Deckow", colors[3]), "2025-01-29", "refunded", 640.50, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1046", "Jacquelyn Robel", "jacquelyn@example.com", avatar_url("Jacquelyn Robel", colors[4]), "2025-01-29", "completed", 39.50, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1045", "Marcus Chen", "marcus@example.com", avatar_url("Marcus Chen", colors[5]), "2025-01-28", "pending", 250.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1044", "Erin Bins", "erin@example.com", avatar_url("Erin Bins", colors[6]), "2025-01-28", "completed", 120.35, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1043", "Gretchen Quitz", "gretchen@example.com", avatar_url("Gretchen Quitz", colors[7]), "2025-01-27", "refunded", 123.50, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1042", "Stewart Kulas", "stewart@example.com", avatar_url("Stewart Kulas", colors[8]), "2025-01-27", "completed", 85.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1041", "Olivia Parker", "olivia@example.com", avatar_url("Olivia Parker", colors[9]), "2025-01-26", "pending", 175.25, "unpaid", now, now),

        # Mid-January orders
        (str(uuid.uuid4()), "#ORD1040", "John Smith", "john@example.com", avatar_url("John Smith", colors[0]), "2025-01-25", "pending", 45.00, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1039", "Jane Doe", "jane@example.com", avatar_url("Jane Doe", colors[1]), "2025-01-25", "completed", 220.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1038", "Bob Wilson", "bob@example.com", avatar_url("Bob Wilson", colors[2]), "2025-01-24", "pending", 75.25, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1037", "Alice Brown", "alice@example.com", avatar_url("Alice Brown", colors[3]), "2025-01-24", "completed", 150.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1036", "Charlie Davis", "charlie@example.com", avatar_url("Charlie Davis", colors[4]), "2025-01-23", "refunded", 89.99, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1035", "Diana Miller", "diana@example.com", avatar_url("Diana Miller", colors[5]), "2025-01-23", "completed", 199.99, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1034", "Edward Garcia", "edward@example.com", avatar_url("Edward Garcia", colors[6]), "2025-01-22", "pending", 55.50, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1033", "Fiona Martinez", "fiona@example.com", avatar_url("Fiona Martinez", colors[7]), "2025-01-22", "completed", 310.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1032", "George Lee", "george@example.com", avatar_url("George Lee", colors[8]), "2025-01-21", "completed", 67.80, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1031", "Hannah White", "hannah@example.com", avatar_url("Hannah White", colors[9]), "2025-01-21", "pending", 125.00, "unpaid", now, now),

        # Early January orders
        (str(uuid.uuid4()), "#ORD1030", "Ivan Taylor", "ivan@example.com", avatar_url("Ivan Taylor", colors[0]), "2025-01-20", "refunded", 45.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1029", "Julia Anderson", "julia@example.com", avatar_url("Julia Anderson", colors[1]), "2025-01-19", "completed", 89.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1028", "Kevin Thompson", "kevin@example.com", avatar_url("Kevin Thompson", colors[2]), "2025-01-19", "pending", 320.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1027", "Laura Jackson", "laura@example.com", avatar_url("Laura Jackson", colors[3]), "2025-01-18", "completed", 55.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1026", "Michael Harris", "michael@example.com", avatar_url("Michael Harris", colors[4]), "2025-01-18", "refunded", 199.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1025", "Nina Clark", "nina@example.com", avatar_url("Nina Clark", colors[5]), "2025-01-17", "pending", 78.50, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1024", "Oscar Lewis", "oscar@example.com", avatar_url("Oscar Lewis", colors[6]), "2025-01-17", "completed", 145.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1023", "Patricia Young", "patricia@example.com", avatar_url("Patricia Young", colors[7]), "2025-01-16", "completed", 230.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1022", "Quinn Walker", "quinn@example.com", avatar_url("Quinn Walker", colors[8]), "2025-01-16", "pending", 65.00, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1021", "Rachel Hall", "rachel@example.com", avatar_url("Rachel Hall", colors[9]), "2025-01-15", "refunded", 110.00, "paid", now, now),

        # Additional orders for comprehensive testing
        (str(uuid.uuid4()), "#ORD1020", "Samuel Allen", "samuel@example.com", avatar_url("Samuel Allen", colors[0]), "2025-01-14", "completed", 450.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1019", "Tina King", "tina@example.com", avatar_url("Tina King", colors[1]), "2025-01-14", "pending", 92.50, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1018", "Victor Wright", "victor@example.com", avatar_url("Victor Wright", colors[2]), "2025-01-13", "completed", 180.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1017", "Wendy Scott", "wendy@example.com", avatar_url("Wendy Scott", colors[3]), "2025-01-13", "refunded", 75.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1016", "Xavier Green", "xavier@example.com", avatar_url("Xavier Green", colors[4]), "2025-01-12", "pending", 285.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1015", "Yolanda Adams", "yolanda@example.com", avatar_url("Yolanda Adams", colors[5]), "2025-01-12", "completed", 67.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1014", "Zachary Baker", "zachary@example.com", avatar_url("Zachary Baker", colors[6]), "2025-01-11", "pending", 142.00, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1013", "Abigail Carter", "abigail@example.com", avatar_url("Abigail Carter", colors[7]), "2025-01-11", "completed", 98.50, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1012", "Benjamin Nelson", "benjamin@example.com", avatar_url("Benjamin Nelson", colors[8]), "2025-01-10", "refunded", 210.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1011", "Catherine Hill", "catherine@example.com", avatar_url("Catherine Hill", colors[9]), "2025-01-10", "completed", 335.00, "paid", now, now),

        # Edge cases: completed but unpaid (ongoing), various amounts
        (str(uuid.uuid4()), "#ORD1010", "Daniel Moore", "daniel@example.com", avatar_url("Daniel Moore", colors[0]), "2025-01-09", "completed", 15.99, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1009", "Emily Taylor", "emily@example.com", avatar_url("Emily Taylor", colors[1]), "2025-01-09", "completed", 999.99, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1008", "Frank Robinson", "frank@example.com", avatar_url("Frank Robinson", colors[2]), "2025-01-08", "pending", 1250.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1007", "Grace Martinez", "grace@example.com", avatar_url("Grace Martinez", colors[3]), "2025-01-08", "refunded", 55.50, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1006", "Henry Anderson", "henry@example.com", avatar_url("Henry Anderson", colors[4]), "2025-01-07", "completed", 420.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1005", "Isabella Thomas", "isabella@example.com", avatar_url("Isabella Thomas", colors[5]), "2025-01-07", "pending", 88.00, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1004", "James Jackson", "james@example.com", avatar_url("James Jackson", colors[6]), "2025-01-06", "completed", 156.75, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1003", "Katherine White", "katherine@example.com", avatar_url("Katherine White", colors[7]), "2025-01-06", "refunded", 299.00, "paid", now, now),
        (str(uuid.uuid4()), "#ORD1002", "Liam Harris", "liam@example.com", avatar_url("Liam Harris", colors[8]), "2025-01-05", "pending", 47.25, "unpaid", now, now),
        (str(uuid.uuid4()), "#ORD1001", "Mia Martin", "mia@example.com", avatar_url("Mia Martin", colors[9]), "2025-01-05", "completed", 185.00, "paid", now, now),
    ]

    cursor.executemany("""
        INSERT INTO orders (id, order_number, customer_name, customer_email, customer_avatar, order_date, status, total_amount, payment_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, mock_orders)

    # Record this migration
    cursor.execute("INSERT INTO _migrations (name) VALUES (?)", ("002_create_orders_table",))

    conn.commit()
    conn.close()
    print("Migration 002_create_orders_table applied successfully.")


def downgrade():
    """Revert the migration."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Drop orders table
    cursor.execute("DROP TABLE IF EXISTS orders")

    # Remove migration record
    cursor.execute("DELETE FROM _migrations WHERE name = ?", ("002_create_orders_table",))

    conn.commit()
    conn.close()
    print("Migration 002_create_orders_table reverted successfully.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run database migration")
    parser.add_argument(
        "action",
        choices=["upgrade", "downgrade"],
        help="Migration action to perform"
    )

    args = parser.parse_args()

    if args.action == "upgrade":
        upgrade()
    elif args.action == "downgrade":
        downgrade()
