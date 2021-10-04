from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.db.utils import OperationalError

# from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_wait_database():
    with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
        gi.return_value = True
        call_command("wait_for_db")
        assert gi.call_count == 1


@patch("time.sleep", return_value=None)
def test_wait_for_db(ts):
    """Test waiting for db"""

    with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
        gi.side_effect = [OperationalError] * 5 + [True]
        call_command("wait_for_db")
        assert gi.call_count == 6
