import sqlite3

class Database:
    def __init__(self, dbname="user_data.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            stickers TEXT,
            stickersRepeat TEXT,
            mode INTEGER
        );
        """)

        self.conn.commit()
    
    def dict_factory(self, row):
        d = {}
        for idx, col in enumerate(self.cursor.description):
            d[col[0]] = row[idx]
        return d
    
    def addUser(self, userId):
        user = self.cursor.execute("SELECT * FROM users where id=?", (userId,)).fetchone()

        if(user == None):
            self.conn.execute("""
                INSERT INTO users (id, stickers, stickersRepeat, mode)
                VALUES (?, ?, ?, ?);
            """, (userId, None, None, 0))
            self.conn.commit()

    def setMode(self, userId, mode):
        self.conn.execute("""
            UPDATE users
            SET mode = ?
            WHERE id = ?
        """, (mode, userId))
        self.conn.commit()

    def setStickers(self, userId, stickers):
        self.conn.execute("""
            UPDATE users
            SET stickers = ?
            WHERE id = ?
        """, (stickers, userId))
        self.conn.commit()
    
    def setStickersRepeat(self, userId, stickersRepeat):
        self.conn.execute("""
            UPDATE users
            SET stickersRepeat = ?
            WHERE id = ?
        """, (stickersRepeat, userId))
        self.conn.commit()
    
    def getData(self, userId):
        return(self.dict_factory(self.cursor.execute("SELECT * FROM users where id=?", (userId,)).fetchone()))