
import pytest
from datetime import datetime, timedelta, timezone
from app.models.grant import Grant
from app.api.grants import normalize_datetime

# Unit test for expiration rule
def test_expiration_rule():
    with pytest.raises(ValueError):
        Grant(
            expires_at=datetime.utcnow() - timedelta(minutes=1)
        )


def test_normalize_datetime_converts_timezone_aware_to_naive_utc():
    aware = datetime(2026, 7, 3, 10, 19, 48, 688000, tzinfo=timezone.utc)

    normalized = normalize_datetime(aware)

    assert normalized == datetime(2026, 7, 3, 10, 19, 48, 688000)
    assert normalized.tzinfo is None
