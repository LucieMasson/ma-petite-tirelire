import unittest
from hypothesis import given, strategies as st
from decimal import Decimal

from service.manager import PiggyBankManager


class TestManager(unittest.TestCase):
    @given(
        coins=st.lists(st.sampled_from([0.01, 0.02, 1, 2])),
        notes=st.lists(st.sampled_from([5, 10, 20, 50, 100])),
    )
    def test_save_piggybank(self, coins, notes):
        m = PiggyBankManager()
        m.create("test")
        m.save(coins, notes)
        # Ici, pour le test, on passe par des "Decimal" pour éviter les erreurs d'arrondis
        self.assertEqual(
            Decimal(str(m.shake())),
            Decimal(
                sum(map(Decimal, [str(c) for c in coins]))
                + sum(map(Decimal, [str(n) for n in notes]))
            ),
        )
