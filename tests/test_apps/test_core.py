"""Tests for abstract core class for console apps."""

import pytest

from protocols.apps import AppProtocol


@pytest.fixture
def dummy_calling_app(test_calling_app_instance):
    return test_calling_app_instance


@pytest.mark.parametrize(
    "handler,ex2handler,err_msg",
    [
        (None, False, None),
        (
            None,
            True,
            "Cannot set always_exit_to_handler to True if no app handler is set!",
        ),
        (dummy_calling_app, False, None),
        (dummy_calling_app, True, None),
    ],
)
def test_console_app_init(
    handler: AppProtocol, ex2handler: bool, err_msg: str | None, test_app_cls
):
    """Test the initialisation of ConsoleApp."""
    if err_msg is not None:
        with pytest.raises(ValueError, match=err_msg):
            test_app_cls(handler, ex2handler)
    else:
        app_instance = test_app_cls(handler, ex2handler)
        assert app_instance.app_name == "Test App"
        assert app_instance.app_handler == handler
        assert app_instance.always_exit_to_handler == ex2handler
