from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from django.db.utils import OperationalError

class CommandTest(TestCase):
    def test_wait_for_db(self):
        call_command('wait_for_db')