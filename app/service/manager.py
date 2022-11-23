from service.orm.models import PiggyBank
from service.orm import crud

from service.exceptions import (
    UnknownPiggyBankError,
    BrokenPiggyBankError,
    UndefinedPiggyBankError,
    UnknownChangeError,
)


class PiggyBankManager:
    """Le point central de notre tirelire. Le manager crée les tirelire, les rempli, les casse"""

    def __init__(self, piggybank_id: int = None):
        """Initialisation de la tirelire, si un id de tirelire est fourni, on essaie de récupérer cette tirelire"""
        self._coins = None
        self._notes = None
        if piggybank_id:
            self.piggybank = crud.get_piggybank(piggybank_id)
            if not self.piggybank:
                raise UnknownPiggyBankError
        else:
            self.piggybank = None

    def _check_existence(self) -> None:
        """Vérifie que la tirelire courante existe bien et n'est pas cassée"""
        if self.piggybank is None:
            raise UndefinedPiggyBankError
        elif self.piggybank.broken:
            raise BrokenPiggyBankError

    def create(self, name: str) -> PiggyBank:
        """Création d'une nouvelle tirelire, avec juste son nom"""
        self.piggybank = crud.add_piggybank(name)
        return self.piggybank

    @staticmethod
    def list_piggybanks() -> list[PiggyBank]:
        """Liste des tirelires existantes"""
        return crud.list_piggybanks()

    def save(self, coins: list[float], notes: list[float]) -> PiggyBank:
        """On met des sous dans la tirelire, sous forme de pièces et de billets"""
        self._check_existence()
        if not self._coins or not self._notes:
            self._coins, self._notes = crud.get_coins_and_notes()

        coins_cent = list(int(c * 100) for c in coins)
        notes_cent = list(int(n * 100) for n in notes)

        unknown_coins = set(coins_cent) - self._coins
        unknown_notes = set(notes_cent) - self._notes
        if unknown_coins or unknown_notes:
            raise UnknownChangeError()

        if coins_cent:
            crud.add_wealth_coins(self.piggybank.id, coins_cent)
        if notes_cent:
            crud.add_wealth_notes(self.piggybank.id, notes_cent)

        return self.piggybank

    def shake(self) -> float:
        """Remuer la tirelire pour connaitre son contenu"""
        self._check_existence()
        amount = crud.shake_piggybank(self.piggybank.id)
        return amount / 100.0

    def smash(self) -> float:
        """Pour casser la tirelire. Elle devient cassée, et on retourne le montant qu'elle contenait"""
        self._check_existence()
        amount = crud.shake_piggybank(self.piggybank.id) / 100.0
        self.piggybank = crud.break_piggybanks(self.piggybank.id)
        return amount
