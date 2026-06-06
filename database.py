import aiosqlite
import asyncio
from datetime import datetime

class Database:
    def __init__(self, db_name="bot_database.db"):
        self.db_name = db_name
    
    async def init_db(self):
        """initialize database tables"""
        async with aiosqlite.connect(self.db_name) as db:
            # users table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    joined_date TEXT,
                    is_banned INTEGER DEFAULT 0,
                    total_forwards INTEGER DEFAULT 0
                )
            ''')
            
            # forwarding stats table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS forward_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    total_messages INTEGER,
                    successful INTEGER,
                    failed INTEGER,
                    start_time TEXT,
                    end_time TEXT,
                    speed REAL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # bot stats table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS bot_stats (
                    id INTEGER PRIMARY KEY,
                    total_users INTEGER DEFAULT 0,
                    total_forwards INTEGER DEFAULT 0,
                    start_time TEXT
                )
            ''')
            
            await db.commit()
    
    async def add_user(self, user_id, username, first_name):
        """add new user to database"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, joined_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, datetime.now().isoformat()))
            await db.commit()
    
    async def get_user(self, user_id):
        """get user from database"""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
                return await cursor.fetchone()
    
    async def update_forward_count(self, user_id):
        """update user forward count"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                UPDATE users SET total_forwards = total_forwards + 1
                WHERE user_id = ?
            ''', (user_id,))
            await db.commit()
    
    async def add_forward_stat(self, user_id, total, successful, failed, start_time, end_time, speed):
        """add forwarding statistics"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                INSERT INTO forward_stats 
                (user_id, total_messages, successful, failed, start_time, end_time, speed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, total, successful, failed, start_time, end_time, speed))
            await db.commit()
    
    async def get_user_stats(self, user_id):
        """get user forwarding statistics"""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('''
                SELECT SUM(total_messages), SUM(successful), SUM(failed), AVG(speed)
                FROM forward_stats WHERE user_id = ?
            ''', (user_id,)) as cursor:
                return await cursor.fetchone()
    
    async def get_total_users(self):
        """get total users count"""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT COUNT(*) FROM users') as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0
    
    async def get_all_users(self):
        """get all users"""
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT user_id FROM users WHERE is_banned = 0') as cursor:
                return await cursor.fetchall()
    
    async def ban_user(self, user_id):
        """ban a user"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
            await db.commit()
    
    async def unban_user(self, user_id):
        """unban a user"""
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
            await db.commit()

db = Database()
