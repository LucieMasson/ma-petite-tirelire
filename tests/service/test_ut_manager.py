import pytest
import unittest
from unittest.mock import patch, MagicMock
from collections import namedtuple

from service.manager import PiggyBankManager
from service.exceptions import UnknownPiggyBankError


FakeTirelire = namedtuple("Tirelire", "id name broken")


class TestManager(unittest.TestCase):
    def test_init_no_data(self):
        m = PiggyBankManager()
        self.assertIsNone(m.piggybank)

    @patch("service.manager.crud.get_piggybank")
    def test_init_data(self, mock_piggybank):
        t = FakeTirelire(id=10, name="cochon", broken=False)
        mock_piggybank.return_value = t
        m = PiggyBankManager(10)
        self.assertEqual(m.piggybank, t)

    @patch("service.manager.crud.get_piggybank")
    def test_init_data_error(self, mock_piggybank):
        mock_piggybank.return_value = None
        with pytest.raises(UnknownPiggyBankError):
            PiggyBankManager(10)

    @patch("service.manager.crud.get_piggybank", MagicMock())
    @patch("service.manager.crud.add_piggybank")
    def test_create_piggybank(self, mock_piggybank):
        t = FakeTirelire(id=10, name="cochon", broken=False)
        mock_piggybank.return_value = t
        m = PiggyBankManager(10)
        self.assertEqual(m.create("cochon"), t)

    @patch("service.manager.crud.get_piggybank")
    @patch("service.manager.crud.shake_piggybank")
    def test_shake_piggybank(self, mock_shake, mock_piggybank):
        t = FakeTirelire(id=10, name="cochon", broken=False)
        mock_piggybank.return_value = t
        value = 50
        mock_shake.return_value = value
        m = PiggyBankManager(10)
        self.assertEqual(m.shake(), value / 100)

    @patch("service.manager.crud.get_piggybank")
    @patch("service.manager.crud.get_coins_and_notes")
    def test_save_piggybank_change_unknown(self, mock_change, mock_piggybank):
        t = FakeTirelire(id=10, name="cochon", broken=False)
        mock_piggybank.return_value = t
        mock_change.return_value = set(), set()
        m = PiggyBankManager(10)
        m.save([], [])
        mock_change.assert_called_once()
