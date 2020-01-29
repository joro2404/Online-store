from database import DB

class Advertisement:
    def __init__(self, id, seller_id, name, description, price, release_date):
        self.id = id
        self.seller_id = seller_id
        self.name = name
        self.description = description
        self.price = price
        self.release_date = release_date
        self.is_available = 1


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM advertisements').fetchall()
            return [Advertisement(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.seller_id, self.name, self.description, self.price, self.release_date, self.is_available)
            db.execute('''
                INSERT INTO advertisements(seller_id, name, description, price, release_date, is_available)
                VALUES (?, ?, ?, ?, ?, ?)''', values)
            return self


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
