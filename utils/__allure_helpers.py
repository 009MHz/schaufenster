import allure
from typing import Any, Iterator, TypeVar, cast
from contextlib import contextmanager
from playwright.async_api import expect

T = TypeVar("T")


@contextmanager
def step(title: str) -> Iterator[None]:
    """
    A properly typed wrapper for allure.step that can be used as a context manager.

    Args:
        title: The title of the step to be shown in the report

    Example:
        ```python
        from utils.allure_helpers import step

        with step("My step description"):
            # actions to perform in this step
        ```
    """
    # Using cast to satisfy type checker while still using the underlying allure step
    allure_step = cast(Any, allure.step(title))
    allure_step.__enter__()
    try:
        yield None
    finally:
        allure_step.__exit__(None, None, None)


class SoftExpect:
    """
    Soft assertions helper that allows tests to continue running after assertion failures.
    All failed assertions are collected and reported at the end.

    Example:
        ```python
        from utils.allure_helpers import Soft

        async def test_example(page):
            soft = Soft()

            await soft.expect(page.get_by_test_id('status')).to_have_text('Success')
            await soft.expect(page.get_by_test_id('eta')).to_have_text('1 day')

            # This will fail with all collected errors if any assertions failed
            soft.assert_all()
        ```
    """

    def __init__(self):
        self.errors = []

    def expect(self, locator):
        """Create a soft expectation wrapper for the given locator."""
        return SoftExpectWrapper(locator, self)

    def assert_all(self):
        """Assert that no soft assertions have failed. If any failed, raise AssertionError with all failures."""
        if self.errors:
            error_message = "\n".join([f"Soft assertion failed: {error}" for error in self.errors])
            raise AssertionError(f"\n{error_message}")


class SoftExpectWrapper:
    """Wrapper class that provides soft assertion methods for Playwright expectations."""

    def __init__(self, locator, soft_instance: SoftExpect):
        self.locator = locator
        self.soft_expect = soft_instance

    async def to_have_text(self, expected: str):
        """Soft assertion for text content."""
        try:
            await expect(self.locator).to_have_text(expected)
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_be_visible(self):
        """Soft assertion for visibility."""
        try:
            await expect(self.locator).to_be_visible()
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_be_hidden(self):
        """Soft assertion for being hidden."""
        try:
            await expect(self.locator).to_be_hidden()
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_be_enabled(self):
        """Soft assertion for being enabled."""
        try:
            await expect(self.locator).to_be_enabled()
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_be_disabled(self):
        """Soft assertion for being disabled."""
        try:
            await expect(self.locator).to_be_disabled()
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_have_value(self, expected: str):
        """Soft assertion for input value."""
        try:
            await expect(self.locator).to_have_value(expected)
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_contain_text(self, expected: str):
        """Soft assertion for containing text."""
        try:
            await expect(self.locator).to_contain_text(expected)
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_have_attribute(self, name: str, value: str):
        """Soft assertion for having specific attribute with value."""
        try:
            await expect(self.locator).to_have_attribute(name, value)
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_have_class(self, expected: str):
        """Soft assertion for having specific CSS class."""
        try:
            await expect(self.locator).to_have_class(expected)
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))

    async def to_have_count(self, count: int):
        """Soft assertion for element count."""
        try:
            await expect(self.locator).to_have_count(count)
        except AssertionError as e:
            self.soft_expect.errors.append(str(e))
