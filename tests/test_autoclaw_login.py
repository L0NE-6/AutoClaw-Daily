"""AutoClaw login contract regressions with fake HTTP responses."""
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import autoclaw_login as login


class LoginContractTests(unittest.TestCase):
    def test_code_is_normalized_to_integer(self):
        self.assertEqual(123456, login.normalize_code("123456"))

    def test_desktop_login_contract(self):
        response = Mock(status_code=200)
        response.json.return_value = {
            "code": 0,
            "data": {
                "access_token": "Bearer access-token",
                "refresh_token": "refresh-token",
            },
        }
        with patch.object(login, "request", return_value=response) as request, \
                patch.object(login, "log"):
            credentials = login.login_with_code(
                "phone-for-test", 123456, "device-for-test")

        args, kwargs = request.call_args
        self.assertEqual("POST", args[0])
        self.assertEqual(login.CN_BASE + "/userapi/v1/agent-login", args[1])
        self.assertEqual(123456, kwargs["body"]["code"])
        self.assertEqual("win", kwargs["body"]["platform"])
        self.assertEqual("access-token", credentials["token"])


if __name__ == "__main__":
    unittest.main()
