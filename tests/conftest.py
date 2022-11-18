import pytest

UT_TAG_CONVENTION = "test_ut"
FT_TAG_CONVENTION = "test_ft"


def pytest_collection_modifyitems(items):
    for item in items:
        if UT_TAG_CONVENTION in item.nodeid:
            item.add_marker(pytest.mark.ut)

        if FT_TAG_CONVENTION in item.nodeid:
            item.add_marker(pytest.mark.ft)
