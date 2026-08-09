"""Tests for pydantic menu models."""

import re

import pytest

from models.menu import MenuItem


@pytest.mark.parametrize(
    "mid,desc,calla,err_msg",
    [
        (-1, "", "", "Input should be greater than or equal to 0"),
        (0, "", "", "String should have at least 1 character"),
        (
            1,
            "valid description",
            "invalid call attr",
            "String should match pattern '^[a-z_]+$'",
        ),
        (
            2,
            "valid description",
            "invalid start valid_call_attr",
            "String should match pattern '^[a-z_]+$'",
        ),
        (
            3,
            "valid descrioption",
            "valid_start invalid end",
            "String should match pattern '^[a-z_]+$'",
        ),
        (4, "valid description", "valid_call_attr", None),
    ],
)
def test_menu_item_validation(
    mid: int, desc: str, calla: str, err_msg: str | None
) -> None:
    """Test the validity of menu items."""
    if err_msg is not None:
        with pytest.raises(ValueError, match=re.escape(err_msg)):
            MenuItem(menu_id=mid, description=desc, call_attr=calla)
    else:
        item = MenuItem(menu_id=mid, description=desc, call_attr=calla)
        assert item.menu_id == mid
        assert item.description == desc
        assert item.call_attr == calla


def test_menu_item_check_call_attr(
    test_menu_item_test_method: MenuItem,
    test_menu_item_other_test_method: MenuItem,
    test_menu_item_exit: MenuItem,
    test_calling_app_instance,
) -> None:
    """Test validity check of menu items call attribute."""
    for item in [
        test_menu_item_test_method,
        test_menu_item_other_test_method,
        test_menu_item_exit,
    ]:
        item.check_call_attr_for_app_object(test_calling_app_instance)
    wrong_item = MenuItem(
        menu_id=0, description="Non-existing method", call_attr="_non_existing_method"
    )
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"MenuItem {wrong_item} does not have a valid call attribute for class {test_calling_app_instance.__class__.__name__}."
        ),
    ):
        wrong_item.check_call_attr_for_app_object(test_calling_app_instance)


def test_menu_item_runs_calls(
    test_menu_item_test_method: MenuItem,
    test_menu_item_other_test_method: MenuItem,
    test_calling_app_instance,
    capsys,
) -> None:
    """Test the runs of menu items."""
    for item in [test_menu_item_test_method, test_menu_item_other_test_method]:
        item.run_call(test_calling_app_instance)
        captured = capsys.readouterr()
        assert captured.out.strip() == f"Running {item.call_attr} for TestApp."
