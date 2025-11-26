import os
import asyncio
import allure
from dotenv import load_dotenv


def pytest_generate_tests_handler(metafunc):
    """Generate tests with platform parameters based on CLI options."""
    # Check if the test function has a platform parameter
    if "platform" in metafunc.fixturenames:
        platform_option = metafunc.config.getoption("platform")

        if platform_option == "mobile":
            platforms = ["mobile"]
        elif platform_option == "desktop":
            platforms = ["desktop"]
        elif platform_option == "all":
            platforms = ["desktop", "mobile"]
        else:
            # Default behavior: run only desktop tests when no platform specified
            platforms = ["desktop"]

        metafunc.parametrize("platform", platforms, scope="function")


def configure_environment(config):
    """Configure environment variables from CLI options."""
    load_dotenv(override=True)  # Force override existing env vars

    # Override with command line options
    os.environ["env"] = config.getoption("env")
    os.environ["mode"] = config.getoption("mode") or "local"
    os.environ["headless"] = str(config.getoption("headless"))

    # Set TEST_ENV for API configuration
    test_env = config.getoption("test_env") or config.getoption("env")
    os.environ["TEST_ENV"] = test_env

    # Set logging flag for API debugging
    log_enabled = config.getoption("log")
    os.environ["API_DEBUG_LOG"] = str(log_enabled).lower()

    # Store options for global access
    platform_option = config.getoption("platform")
    config._platform_option = platform_option
    config._test_env = test_env
    config._log_enabled = log_enabled


def add_pytest_options(parser):
    """Add custom pytest command line options."""
    parser.addoption(
        "--env", action="store", default="test", help="Specify the test environment"
    )
    parser.addoption(
        "--test-env",
        action="store",
        default="qa",
        help="Specify the API test environment: dev, qa, staging, production",
    )
    parser.addoption(
        "--mode",
        help="Specify the execution mode: local, grid, pipeline",
        default="local",
    )
    parser.addoption(
        "--platform",
        help="Specify the platform: desktop, mobile, or all",
        default="desktop",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode",
    )
    parser.addoption(
        "--log",
        action="store_true",
        default=False,
        help="Enable detailed logging for API requests and responses",
    )


def handle_test_screenshot(item, rep):
    """Handle screenshot capture based on test result and CLI options."""
    if rep.when != "call":
        return

    screenshot_mode = item.config.getoption("--screenshot", default="off")
    should_screenshot = False

    if screenshot_mode == "on":
        should_screenshot = True
    elif screenshot_mode == "only-on-failure" and rep.failed:
        should_screenshot = True

    if should_screenshot:
        screenshot_path = os.path.join("reports/screenshots", f"{item.name}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

        try:
            page = item.funcargs.get("page") or item.funcargs.get("auth_page")
            if page:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    page.screenshot(path=screenshot_path, full_page=True)
                )
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
