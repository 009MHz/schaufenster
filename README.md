# Schaufenster - Modern Test Automation Framework

[![API Tests](https://github.com/009MHz/schaufenster/actions/workflows/test-api.yml/badge.svg)](https://github.com/009MHz/schaufenster/actions/workflows/test-api.yml)
[![Web UI Tests](https://github.com/009MHz/schaufenster/actions/workflows/test-web.yml/badge.svg)](https://github.com/009MHz/schaufenster/actions/workflows/test-web.yml)
[![Smoke Tests](https://github.com/009MHz/schaufenster/actions/workflows/test-smoke.yml/badge.svg)](https://github.com/009MHz/schaufenster/actions/workflows/test-smoke.yml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-ready, scalable test automation framework built with **modern async Python**, featuring parallel test execution, comprehensive reporting, and full CI/CD integration. Designed to demonstrate enterprise-level testing practices and architecture.

## Demo Applications Under Test

- **Web UI**: [DemoQA](https://demoqa.com) & [SauceDemo](https://www.saucedemo.com)
- **API**: [Reqres.in](https://reqres.in)

## 🎯 Key Features

### Architecture Highlights
- ✅ **Async-First Design** - Full async/await implementation for optimal performance
- ✅ **Parallel-Safe** - Function-scoped fixtures ensuring complete test isolation
- ✅ **Page Object Model** - Clean separation of concerns with dynamic POM implementation
- ✅ **CI/CD Ready** - GitHub Actions workflows with automated reporting
- ✅ **Docker Support** - Containerized execution for consistency across environments
- ✅ **Multi-Platform** - Desktop & mobile device emulation support

### Technology Stack
- **Python 3.11+** - Modern async Python with type hints
- **Playwright** - Async browser automation with auto-waiting
- **Pytest** - Async test framework with xdist for parallelization
- **Allure** - Enterprise reporting with GitHub Pages integration
- **Docker** - Containerized test execution

### What This Framework Demonstrates
- **Web UI Testing**: Form interactions, e-commerce flows, element manipulation
- **API Testing**: REST API validation, authentication, CRUD operations
- **Parallel Execution**: pytest-xdist with proper fixture isolation
- **CI/CD Integration**: Automated pipeline with test reports
- **Test Organization**: Clean architecture with reusable components

## ⚡ Quick Start

### Local Setup
```bash
# Clone repository
git clone https://github.com/009MHz/schaufenster.git
cd schaufenster

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run tests
pytest tests/web/saucedemo -n auto  # SauceDemo tests in parallel
pytest tests/api -n auto             # API tests in parallel
pytest -m smoke                      # Smoke tests only
```

### Docker Execution
```bash
# Build and run tests
docker-compose up tests

# View Allure reports
docker-compose up allure allure-ui
# Visit http://localhost:5252 for reports
```

## 🏃 Running Tests

### Web UI Tests
```bash
# Run all web tests
pytest tests/web --platform=desktop --headless -n=auto

# SauceDemo specific
pytest tests/web/saucedemo -v

# DemoQA specific
pytest tests/web/demoqa -v

# Mobile emulation
pytest tests/web --platform=mobile --headless
```

### API Tests
```bash
# Run all API tests
pytest tests/api -n=auto

# Specific API client
pytest tests/api/reqres/test_users_api.py
pytest tests/api/reqres/test_resources_api.py

# With different environment
pytest tests/api --test-env=qa
```

### Test Selection
```bash
# By marker
pytest -m smoke          # Smoke tests
pytest -m regression     # Regression suite
pytest -m api           # API tests only
pytest -m ui            # UI tests only

# Parallel execution
pytest tests -n=auto     # Auto-detect workers
pytest tests -n=4        # 4 workers

# With Allure reporting
pytest tests --alluredir=reports/allure
allure serve reports/allure
```

## 📊 Reporting & Analytics

### Report Types Available
The framework generates multiple types of reports to serve different stakeholder needs:

#### Allure Reports (Recommended)
- **Interactive Dashboard**: Real-time test execution monitoring with filters and search
- **Visual Documentation**: Screenshots, videos, and step-by-step test execution flows
- **Historical Trends**: Test stability analysis and performance metrics over time
- **Categorization**: Tests organized by feature, severity, and execution status
- **Integration Ready**: Compatible with CI/CD pipelines and notification systems

#### HTML Reports
- **Standalone Reports**: Self-contained HTML files that can be shared easily
- **Summary Statistics**: Quick overview of test execution results and coverage
- **Failure Details**: Detailed error information and debugging context

### Generate Reports:
```bash
# Allure reports with screenshots
pytest --alluredir=reports
allure serve reports

# HTML reports
pytest --html=reports/report.html
```

### Report Features
- **Screenshot Capture**: Automatic screenshots on test failures for visual debugging
- **Video Recording**: Full test execution videos for complex failure analysis
- **Log Integration**: Comprehensive application and test execution logs
- **Performance Metrics**: Execution time analysis and bottleneck identification
- **Custom Annotations**: Business context and requirements traceability

## 📁 Project Architecture

### Directory Structure
```
schaufenster/
├── .github/workflows/       # CI/CD pipelines
│   ├── test-api.yml        # API test automation
│   ├── test-web.yml        # Web UI test automation
│   ├── test-smoke.yml      # Quick smoke tests
│   └── test-all.yml        # Full regression suite
│
├── sources/                 # Page Object Model & API Clients
│   ├── web/                # Web page objects
│   │   ├── base_page.py   # Base page with common methods
│   │   ├── demoqa/        # DemoQA page objects
│   │   │   ├── elements_page.py
│   │   │   └── forms_page.py
│   │   └── saucedemo/     # SauceDemo page objects
│   │       ├── login_page.py
│   │       ├── inventory_page.py
│   │       └── cart_page.py
│   └── api/               # API clients
│       ├── base_client.py # Base async API client
│       └── reqres/        # Reqres.in clients
│           ├── users_client.py
│           └── resources_client.py
│
├── tests/                  # Test implementations
│   ├── fixtures/          # Pytest fixtures
│   │   ├── api_fixtures.py
│   │   └── web_fixtures.py
│   ├── web/               # Web UI tests
│   │   ├── demoqa/
│   │   └── saucedemo/
│   │       ├── test_login.py
│   │       └── test_shopping.py
│   └── api/               # API tests
│       └── reqres/
│           ├── test_users_api.py
│           └── test_resources_api.py
│
├── utils/                  # Configuration & utilities
│   ├── web_browser_config.py  # Browser setup
│   ├── api_config.py          # API configuration
│   ├── __pytest_config.py     # Pytest options
│   └── __allure_helpers.py    # Allure step helpers
│
├── conftest.py            # Global fixtures
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Dependencies
├── Dockerfile            # Container definition
├── docker-compose.yml    # Multi-service orchestration
└── README.md             # Documentation
```

### Design Principles

#### 1. Async-First Architecture
All page objects and API clients use async/await:
```python
async def test_login(login_page):
    await login_page.navigate_to_login()
    await login_page.login_as_standard_user()
    assert await login_page.is_on_inventory_page()
```

#### 2. Parallel-Safe Fixtures
Function-scoped fixtures ensure test isolation:
```python
@pytest.fixture(scope="function")
async def api_context(playwright):
    context = await playwright.request.new_context()
    yield context
    await context.dispose()
```

#### 3. Page Object Model
Clean separation of page interactions from test logic:
```python
class LoginPage(BasePage):
    async def login(self, username, password):
        await self.fill(self.page.locator("#user-name"), username)
        await self.fill(self.page.locator("#password"), password)
        await self.click(self.page.locator("#login-button"))
```

#### 4. Reusable API Clients
Base client with common HTTP methods:
```python
class UsersClient(BaseAPIClient):
    async def get_user(self, user_id: int):
        return await self.get(f"/users/{user_id}")
```

## 📝 Test ID Naming Conventions

All test cases follow a structured naming convention to ensure consistency, traceability, and scalability. 

### Quick Reference

#### WEB Tests (UI)
```
WEB-<Page>-<Section>-<Number>
```
**Example**: `WEB-DASH-001` → Dashboard test #001

#### API Tests
```
<Domain>-<Endpoint>-<Status>-<Serial>-<Country>-<Partner>
```
**Examples**:
- `MOB-LOGIN-200-001` → Mobile login success test
- `WAP-PAYM-200-001-TH-PERT` → Pertamina payment methods in Thailand

**Note**: Country and Partner codes are optional – only use when testing country/partner-specific behavior.

### Common Test ID Examples

| Test ID | Description |
|---------|-------------|
| `WEB-DASH-001` | Dashboard loads correctly |
| `MOB-LOGIN-200-001` | Mobile app valid login |
| `MOB-LOGIN-401-001` | Mobile app invalid password |
| `WAP-DONA-200-001` | Web app donation request |
| `WAP-OILRWD-200-001-PERT` | Pertamina oil rewards |
| `MOB-PAYM-200-001-TH` | Payment methods - Thailand |

### Key Principles
- **Keep IDs Stable**: Never renumber test IDs when adding new tests
- **Use 3-digit serial numbers**: 001, 002, 003...
- **Add optional components only when needed**: Start simple, add country/partner codes only for specific tests
- **MOB vs WAP**: Keep separate even though they use same endpoints (different client setups)

For detailed guidelines, examples, and decision trees, refer to the full [Test ID Naming Conventions](tests/Test%20ID%20Naming%20Conventions.md) document.

## 🎯 Best Practices & Guidelines

### Test Development Standards
- **Test Independence**: Each test should run independently without dependencies on other tests
- **Clear Naming**: Test names should clearly describe what functionality is being tested
- **Proper Assertions**: Use meaningful assertions that provide clear failure messages
- **Data Management**: Use fixtures and test data factories for consistent test data setup
- **Error Handling**: Implement robust error handling and meaningful error messages
- **Test IDs**: Follow the established naming convention for all new tests

### Code Quality Standards
- **Type Hints**: Use Python type hints for better code documentation and IDE support
- **Documentation**: Include docstrings for complex test scenarios and helper functions
- **Code Reviews**: All test code should be reviewed before merging to ensure quality
- **Version Control**: Follow conventional commit messages and branching strategies

### Execution Guidelines
- **Local Testing**: Always run tests locally before committing changes
- **Incremental Testing**: Run relevant test subsets during development for faster feedback
- **Full Regression**: Execute complete test suite before major releases
- **Environment Consistency**: Use consistent test environments across team members

## 🚀 CI/CD Integration

### GitHub Actions Workflows

The framework includes comprehensive CI/CD pipelines:

#### 1. **API Tests** (`.github/workflows/test-api.yml`)
- Triggers on push to API-related files
- Runs on PR to main/develop branches
- Manual dispatch with environment selection
- Publishes results to GitHub Pages

#### 2. **Web UI Tests** (`.github/workflows/test-web.yml`)
- Supports platform selection (desktop/mobile/all)
- Headless browser execution
- Screenshot capture on failures
- Allure report generation

#### 3. **Smoke Tests** (`.github/workflows/test-smoke.yml`)
- Quick validation on every PR
- Runs critical path tests
- Fast feedback loop (~2-5 minutes)

#### 4. **Full Test Suite** (`.github/workflows/test-all.yml`)
- Scheduled daily execution (2 AM UTC)
- Matrix strategy for parallel execution
- Combined report generation
- Historical trend analysis

### Viewing Test Reports

After workflow execution, reports are automatically published to GitHub Pages:
- **API Tests**: `https://<username>.github.io/<repo>/api-tests`
- **Web Tests**: `https://<username>.github.io/<repo>/web-tests`
- **Full Suite**: `https://<username>.github.io/<repo>/full-suite`

### Local Docker Execution

```bash
# Run tests in container
docker-compose up tests

# View Allure reports
docker-compose up allure allure-ui

# Clean up
docker-compose down
```

## 🎯 Best Practices

### Async & Parallelism
✅ **DO:**
- Use function-scoped fixtures
- Always use `async/await` in tests
- Let pytest-xdist handle worker distribution
- Ensure tests are stateless

❌ **DON'T:**
- Share state between tests
- Use session/module scoped mutable fixtures
- Depend on test execution order
- Use time.sleep (use await page.wait_for_* instead)

### Page Object Model
✅ **DO:**
- Keep page objects free of assertions
- Return data from page methods
- Use modern locators (get_by_role, get_by_text)
- Inherit from BasePage

❌ **DON'T:**
- Put test logic in page objects
- Assert in page object methods
- Use xpath/css selectors when better options exist
- Hardcode waits

### Test Organization
✅ **DO:**
- Follow AAA pattern (Arrange, Act, Assert)
- Use Allure steps for readability
- One test = one scenario
- Meaningful test IDs and names

❌ **DON'T:**
- Create mega tests testing multiple scenarios
- Skip test documentation
- Ignore failing tests
- Forget to mark tests (@pytest.mark.api, etc.)

## 📚 Learning Resources

### Key Concepts Demonstrated

1. **Async Python Testing**
   - `async/await` syntax throughout
   - Proper fixture lifecycle management
   - Concurrent test execution

2. **Page Object Model**
   - Base page abstraction
   - Method chaining for readability
   - No business logic in page objects

3. **API Testing**
   - RESTful API validation
   - Request/response handling
   - Status code verification

4. **CI/CD Pipeline**
   - GitHub Actions workflows
   - Automated report publishing
   - Multi-environment support

### File References

- **Base implementations**: `sources/web/base_page.py`, `sources/api/base_client.py`
- **Example tests**: `tests/web/saucedemo/test_login.py`, `tests/api/reqres/test_users_api.py`
- **Fixtures**: `tests/fixtures/web_fixtures.py`, `tests/fixtures/api_fixtures.py`
- **CI/CD**: `.github/workflows/*.yml`

## 🤝 Contributing

Contributions welcome! This is a portfolio/demonstration project showing modern test automation practices.

### Areas for Enhancement
- Additional page objects for DemoQA
- Mobile device testing (Appium integration)
- Visual regression testing
- Performance testing with Locust
- Database validation

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**009MHz**
- GitHub: [@009MHz](https://github.com/009MHz)
- Portfolio Project: Demonstrating modern test automation architecture

---

**Built with** ❤️ **using Python, Playwright, and modern async patterns**
