"""test custom django management commands."""

from unittest.mock import patch  # patch to mock behaviour

from psycopg2 import OperationalError as Psycopg2Error  # error which we might get if the db is not ready

from django.core.management import call_command  # helper function to simulate the call fo a command by name
from django.db.utils import OperationalError  # another error which we might get if the db is not ready
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')  # we provide the path for the Command.check method
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """test waiting for the database if database ready"""
        patched_check.return_value = True  # this means when check is called, we return the true value

        call_command('wait_for_db')  # we call the wait_for_db command

        patched_check.assert_called_once_with(databases=['default'])  # the mock value of check is called by default

    def test_wait_for_db_delay(self, patched_check):
        """test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')


