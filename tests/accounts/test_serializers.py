import pytest
from rest_framework.exceptions import ValidationError

from accounts.serializers import SignUpSerializer


def test_validate_password():
    serializer = SignUpSerializer()

    valid_password = "password"
    assert serializer.validate_password(valid_password) == valid_password

    with pytest.raises(ValidationError, match="パスワードは8文字以上で入力してください"):
        serializer.validate_password("1234567")
