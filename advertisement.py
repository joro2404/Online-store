from database import DB
from user import User

class Advertisement:
    def __init__(self, id, seller_id, buyer_id, name, description, price, release_date, is_available):
        self.id = id
        self.seller_id = seller_id
        self.buyer_id = buyer_id
        self.name = name
        self.description = description
        self.price = price
        self.release_date = release_date
        self.is_available = is_available


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM advertisements').fetchall()
            return [Advertisement(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.seller_id, self.buyer_id, self.name, self.description, self.price, self.release_date, self.is_available)
            db.execute('''
                INSERT INTO advertisements(seller_id, buyer_id, name, description, price, release_date, is_available)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', values)
            return self

    @staticmethod
    def get_seller_name(seller_id):
        with DB() as db:
            seller_name = db.execute('SELECT username FROM users WHERE id = ?', (seller_id,)).fetchone()
            return int("".join(map(str, seller_name)))

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM advertisements WHERE id = ?',(id,)).fetchone()
            return Advertisement(*row)

    @staticmethod
    def get_by_seller_id(seller_id):
        with DB() as db:
            rows = db.execute('SELECT * FROM advertisements WHERE seller_id = ?', (seller_id,)).fetchall()
            return [Advertisement(*row) for row in rows]

    @staticmethod
    def get_buyer_info(buyer_id):
        with DB() as db:
            buyer = db.execute('SELECT * FROM users WHERE id = ?', (buyer_id,)).fetchone()
            return User(*buyer)

    @staticmethod
    def find_by_name(name):
        if not name:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM advertisements WHERE name = ?',
                (name,)
            ).fetchone()
            if row:
                return Advertisement(*row)

    def save(self):
        with DB() as db:
            values = (self.name, self.description, self.price, self.id)
            db.execute('UPDATE advertisements SET name = ?, description = ?, price = ? WHERE id = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM advertisements WHERE id = ?', (self.id,))
            return self

    def buy(self,buyer_id):
        with DB() as db:
            db.execute('UPDATE advertisements SET buyer_id = ?, is_available = ? WHERE id = ?', (buyer_id, 0, self.id,))
            return self

    
