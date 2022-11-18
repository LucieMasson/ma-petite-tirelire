from service.orm.models import Tirelire, Richesse, Monnaie
from service.orm.database import SessionLocal


class TirelireManager:
    def __init__(self, tirelire_id: int = None):
        with SessionLocal() as session:
            self.monnaie = session.query(Monnaie).all()
            if tirelire_id:
                self.tirelire = (
                    session.query(Tirelire).filter_by(id=tirelire_id).first()
                )
                if not self.tirelire:
                    raise Exception(f"La tirelire {tirelire_id} n" "existe pas")
            else:
                self.tirelire = None

    def create(self, name: str) -> Tirelire:
        with SessionLocal() as session, session.begin():
            t = Tirelire(name=name)
            session.add(t)
        self.tirelire = t
        return self.tirelire

    def save(self, coins: list[int], notes: list[int]) -> Tirelire:
        if self.tirelire is None:
            raise Exception("Pas de tirelire définie")
        elif self.tirelire.broken:
            raise Exception("La tirelire est cassée")

        for coin in coins:
            pass

        return self.tirelire
