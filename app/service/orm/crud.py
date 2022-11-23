from sqlalchemy import delete
from service.orm.models import PiggyBank, Wealth, Change
from service.orm.database import SessionLocal


def get_piggybank(piggybank_id: int) -> PiggyBank:
    """Retourne une tirelire à partir de son ID"""
    with SessionLocal() as session:
        t = session.get(PiggyBank, piggybank_id)
    return t


def get_coins_and_notes() -> (set[int], set[int]):
    """Retourne les pièces et billets qui existent"""
    with SessionLocal() as session:
        result = session.query(Change).filter_by(kind="coin").all()
        coins = set(c.value for c in result)
        result = session.query(Change).filter_by(kind="note").all()
        notes = set(c.value for c in result)

    return coins, notes


def add_piggybank(name: str) -> PiggyBank:
    """Ajoute une tirelire en base de donnée. Cette tirelire est initialement vide"""
    with SessionLocal() as session, session.begin():
        t = PiggyBank(name=name)
        session.add(t)
    return t


def list_piggybanks() -> list[PiggyBank]:
    """Retourne la liste des tirelires existantes"""
    with SessionLocal() as session:
        result = session.query(PiggyBank).all()
    return result


def shake_piggybank(piggybank_id: int) -> int:
    """Retourne les montants dans la tirelire"""
    with SessionLocal() as session, session.begin():
        result = session.query(Wealth).filter_by(piggybank_id=piggybank_id).all()
        _sum = sum(row.change.value for row in result)
    return _sum


def break_piggybanks(piggybank_id: int) -> PiggyBank:
    """Casse la tirelire en changeant le statut broken et en supprimant la richesse"""
    with SessionLocal() as session, session.begin():
        piggybank = session.query(PiggyBank).filter_by(id=piggybank_id).first()
        piggybank.broken = True
        dele = delete(Wealth).where(Wealth.piggybank_id == piggybank_id)
        session.execute(dele)
    return piggybank


def _add_wealth(piggybank_id: int, kind: str, values: list[int]) -> None:
    """Ajoute des pièces ou des billets à la richesse d'une tirelire"""
    with SessionLocal() as session, session.begin():
        changes = (
            session.query(Change)
            .filter_by(kind=kind)
            .filter(Change.value.in_(set(values)))
            .all()
        )
        changes = dict((c.value, c.id) for c in changes)
        w = list(
            Wealth(
                piggybank_id=piggybank_id,
                change_id=changes[c],
            )
            for c in values
        )
        session.bulk_save_objects(w)


def add_wealth_coins(piggybank_id: int, coins: list[int]) -> None:
    return _add_wealth(piggybank_id, "coin", coins)


def add_wealth_notes(piggybank_id: int, notes: list[int]) -> None:
    return _add_wealth(piggybank_id, "note", notes)
