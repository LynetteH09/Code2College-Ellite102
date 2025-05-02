import unittest
from unittest.mock import patch, MagicMock
import main

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        self.banking_system = main.BankingSystem()
        self.banking_system.create_account("Alice", 1000)
        self.banking_system.create_account("Bob", 500)

    def test_create_account(self):
        account = self.banking_system.get_account("Alice")
        self.assertIsNotNone(account)
        self.assertEqual(account.name, "Alice")
        self.assertEqual(account.balance, 1000)

    def test_deposit(self):
        account = self.banking_system.get_account("Alice")
        account.deposit(500)
        self.assertEqual(account.balance, 1500)

    def test_withdraw(self):
        account = self.banking_system.get_account("Bob")
        account.withdraw(200)
        self.assertEqual(account.balance, 300)