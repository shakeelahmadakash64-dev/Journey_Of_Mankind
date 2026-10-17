"""
Journey of Mankind - Player Account & Progress Database
Uses SQLite to store player profiles, epoch progress, biological survival state,
elevation, facing direction, and inventory.
"""

import sqlite3
import os
import sys
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            if getattr(sys, 'frozen', False):
                exe_dir = os.path.dirname(sys.executable)
                test_file = os.path.join(exe_dir, '.perm_test')
                try:
                    with open(test_file, 'w') as f:
                        f.write('1')
                    os.remove(test_file)
                    save_dir = exe_dir
                except Exception:
                    appdata = os.getenv('APPDATA') or os.path.expanduser('~')
                    save_dir = os.path.join(appdata, 'JourneyOfMankind')
                    os.makedirs(save_dir, exist_ok=True)
                db_path = os.path.join(save_dir, 'mankind_data.db')
            else:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(script_dir, '..', 'mankind_data.db')
        self.db_path = os.path.abspath(db_path)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _hash_pin(self, pin):
        return hashlib.sha256(str(pin).encode('utf-8')).hexdigest()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    username TEXT PRIMARY KEY,
                    pin_hash TEXT NOT NULL,
                    current_era INTEGER DEFAULT 1,
                    prologue_completed INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    last_saved TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS character_state (
                    username TEXT PRIMARY KEY,
                    health REAL DEFAULT 100.0,
                    hunger REAL DEFAULT 100.0,
                    thirst REAL DEFAULT 100.0,
                    stamina REAL DEFAULT 100.0,
                    temperature REAL DEFAULT 37.0,
                    pos_x INTEGER DEFAULT 0,
                    pos_y INTEGER DEFAULT 0,
                    elevation INTEGER DEFAULT 0,
                    facing TEXT DEFAULT 'North',
                    FOREIGN KEY(username) REFERENCES players(username)
                )
            ''')

            # Ensure columns exist if older database exists
            cursor.execute("PRAGMA table_info(character_state)")
            cols = [info[1] for info in cursor.fetchall()]
            if 'elevation' not in cols:
                cursor.execute("ALTER TABLE character_state ADD COLUMN elevation INTEGER DEFAULT 0")
            if 'facing' not in cols:
                cursor.execute("ALTER TABLE character_state ADD COLUMN facing TEXT DEFAULT 'North'")
            if 'fatigue' not in cols:
                cursor.execute("ALTER TABLE character_state ADD COLUMN fatigue REAL DEFAULT 0.0")
            if 'morale' not in cols:
                cursor.execute("ALTER TABLE character_state ADD COLUMN morale REAL DEFAULT 90.0")
            if 'social' not in cols:
                cursor.execute("ALTER TABLE character_state ADD COLUMN social REAL DEFAULT 70.0")
            if 'partner_data' not in cols:
                cursor.execute("ALTER TABLE character_state ADD COLUMN partner_data TEXT DEFAULT ''")
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    username TEXT,
                    item_id TEXT,
                    item_name TEXT,
                    quantity INTEGER,
                    PRIMARY KEY(username, item_id),
                    FOREIGN KEY(username) REFERENCES players(username)
                )
            ''')
            conn.commit()

    def register_player(self, username, pin="1234"):
        username = username.strip().capitalize()
        if not username:
            return False, "Player name cannot be empty."
        
        now = datetime.now().isoformat()
        pin_hash = self._hash_pin(pin)
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO players (username, pin_hash, current_era, prologue_completed, created_at, last_saved) VALUES (?, ?, 1, 0, ?, ?)",
                    (username, pin_hash, now, now)
                )
                cursor.execute(
                    "INSERT INTO character_state (username, health, hunger, thirst, stamina, temperature, pos_x, pos_y, elevation, facing, fatigue, morale, social, partner_data) VALUES (?, 100.0, 100.0, 100.0, 100.0, 37.0, 0, 0, 0, 'North', 0.0, 90.0, 70.0, '')",
                    (username,)
                )
                starting_items = [
                    ('flint_stone', 'Flint Stone', 2),
                    ('wood_stick', 'Hardwood Branch', 3),
                    ('wild_berries', 'Wild Berries', 5)
                ]
                for item_id, item_name, qty in starting_items:
                    cursor.execute(
                        "INSERT INTO inventory (username, item_id, item_name, quantity) VALUES (?, ?, ?, ?)",
                        (username, item_id, item_name, qty)
                    )
                conn.commit()
            return True, f"Account '{username}' created successfully!"
        except sqlite3.IntegrityError:
            return False, f"Name '{username}' already exists. Please pick another."

    def login_player(self, username, pin="1234"):
        username = username.strip().capitalize()
        pin_hash = self._hash_pin(pin)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pin_hash FROM players WHERE username = ?", (username,))
            row = cursor.fetchone()
            if not row:
                return False, f"Player '{username}' not found."
            if row[0] != pin_hash:
                return False, "Incorrect PIN."
            return True, f"Welcome, {username}!"

    def list_players(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, current_era, last_saved FROM players ORDER BY last_saved DESC")
            return cursor.fetchall()

    def get_player_data(self, username):
        username = username.strip().capitalize()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_era, prologue_completed FROM players WHERE username = ?", (username,))
            p_row = cursor.fetchone()
            if not p_row:
                return None
            
            cursor.execute("SELECT health, hunger, thirst, stamina, temperature, pos_x, pos_y, elevation, facing, fatigue, morale, social, partner_data FROM character_state WHERE username = ?", (username,))
            c_row = cursor.fetchone()
            
            cursor.execute("SELECT item_id, item_name, quantity FROM inventory WHERE username = ?", (username,))
            inv_rows = cursor.fetchall()
            
            h_val = float(c_row[0]) if (c_row[0] is not None and c_row[0] > 0) else 100.0
            hg_val = float(c_row[1]) if (c_row[1] is not None and c_row[1] > 0) else 100.0
            th_val = float(c_row[2]) if (c_row[2] is not None and c_row[2] > 0) else 100.0
            st_val = float(c_row[3]) if (c_row[3] is not None and c_row[3] > 0) else 100.0
            
            return {
                'username': username,
                'current_era': p_row[0],
                'prologue_completed': bool(p_row[1]),
                'stats': {
                    'health': h_val,
                    'hunger': hg_val,
                    'thirst': th_val,
                    'stamina': st_val,
                    'temperature': c_row[4] if c_row[4] is not None else 37.0,
                    'pos_x': c_row[5],
                    'pos_y': c_row[6],
                    'elevation': c_row[7] if len(c_row) > 7 and c_row[7] is not None else 0,
                    'facing': c_row[8] if len(c_row) > 8 and c_row[8] is not None else 'North',
                    'fatigue': float(c_row[9]) if len(c_row) > 9 and c_row[9] is not None else 0.0,
                    'morale': float(c_row[10]) if len(c_row) > 10 and c_row[10] is not None else 90.0,
                    'social': float(c_row[11]) if len(c_row) > 11 and c_row[11] is not None else 70.0,
                    'partner_data': str(c_row[12]) if len(c_row) > 12 and c_row[12] is not None else ''
                },
                'inventory': [{'id': r[0], 'name': r[1], 'quantity': r[2]} for r in inv_rows]
            }

    def save_player_data(self, username, stats, inventory, current_era=None, prologue_completed=None):
        username = username.strip().capitalize()
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if current_era is not None or prologue_completed is not None:
                updates = ["last_saved = ?"]
                params = [now]
                if current_era is not None:
                    updates.append("current_era = ?")
                    params.append(current_era)
                if prologue_completed is not None:
                    updates.append("prologue_completed = ?")
                    params.append(1 if prologue_completed else 0)
                params.append(username)
                cursor.execute(f"UPDATE players SET {', '.join(updates)} WHERE username = ?", tuple(params))
            else:
                cursor.execute("UPDATE players SET last_saved = ? WHERE username = ?", (now, username))
            
            cursor.execute('''
                UPDATE character_state SET
                    health = ?, hunger = ?, thirst = ?, stamina = ?, temperature = ?, pos_x = ?, pos_y = ?,
                    elevation = ?, facing = ?, fatigue = ?, morale = ?, social = ?, partner_data = ?
                WHERE username = ?
            ''', (
                stats['health'], stats['hunger'], stats['thirst'],
                stats['stamina'], stats['temperature'], stats['pos_x'], stats['pos_y'],
                stats.get('elevation', 0), stats.get('facing', 'North'),
                stats.get('fatigue', 0.0), stats.get('morale', 90.0), stats.get('social', 70.0),
                stats.get('partner_data', ''),
                username
            ))
            
            cursor.execute("DELETE FROM inventory WHERE username = ?", (username,))
            for item in inventory:
                cursor.execute(
                    "INSERT INTO inventory (username, item_id, item_name, quantity) VALUES (?, ?, ?, ?)",
                    (username, item['id'], item['name'], item['quantity'])
                )
            conn.commit()
