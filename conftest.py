import pytest
import asyncio
from playwright.async_api import async_playwright
from utils.web_browser_config import Config, ContextManager
from utils.__pytest_config import (
    pytest_generate_tests_handler as generate_tests_handler,
    configure_environment,
    add_pytest_options,
    handle_test_screenshot,
)

pytest_plugins = [
    "tests.fixtures.api_fixtures",
    "tests.fixtures.web_fixtures",
    ]


def pytest_addoption(parser):
    """Add custom pytest command line options."""
    add_pytest_options(parser)


def pytest_configure(config):
    """Configure environment from CLI options."""
    configure_environment(config)


def pytest_generate_tests(metafunc):
    """Generate tests with platform parameters based on CLI options."""
    generate_tests_handler(metafunc)


@pytest.fixture(scope="function")
async def playwright():
    """Function-scoped playwright instance for worker safety."""
    async with async_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
async def runner(playwright):
    """Function-scoped runner instance for parallel execution safety."""
    runner_instance = Config()
    await runner_instance.setup_browser(playwright)
    yield runner_instance
    if runner_instance.browser:
        await runner_instance.browser.close()


@pytest.fixture(scope="function")
async def browser(runner):
    """Function-scoped browser for parallel execution safety."""
    yield runner.browser


@pytest.fixture()
async def context(runner, request):
    """Create browser context with optional device emulation."""
    context_manager = ContextManager(runner)

    context, _ = await context_manager.create_context(request)
    yield context
    await context_manager.cleanup_context(context)


@pytest.fixture()
async def page(context, runner):
    """Create new page in the current context."""
    context_manager = ContextManager(runner)
    page = await context_manager.create_page(context)
    yield page
    await context_manager.cleanup_page(page)


@pytest.fixture()
async def user_auth(runner):
    page_instance = await runner.setup_auth_page("admin_no_otp")
    yield page_instance
    await runner.capture_handler()
    await page_instance.close()


@pytest.fixture()
async def admin_auth(runner):
    page_instance = await runner.setup_auth_page("admin_otp")
    yield page_instance
    await runner.capture_handler()
    await page_instance.close()


@pytest.fixture()
async def super_auth(runner):
    page_instance = await runner.setup_auth_page("super_admin")
    yield page_instance
    await runner.capture_handler()
    await page_instance.close()


@pytest.fixture(scope="session")
def base_url():
    """Provide base URL based on test environment."""
    from utils.web_browser_config import get_environment_base_url
    return get_environment_base_url()


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set the event loop policy for the test session."""
    return asyncio.get_event_loop_policy()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to handle test reporting and screenshot capture."""
    outcome = yield
    rep = outcome.get_result()
    handle_test_screenshot(item, rep)
