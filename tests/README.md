# Azure VM Migration Pipeline - Test Suite

This directory contains comprehensive pytest unit tests for the Azure VM Migration Pipeline, covering Terraform modules, Ansible playbooks, Azure integrations, and various migration scenarios.

## Test Structure

```
tests/
├── requirements.txt          # Python dependencies for testing
├── pytest.ini               # Pytest configuration
├── conftest.py              # Shared fixtures and configuration
├── test_terraform_validation.py    # Terraform configuration tests
├── test_ansible_validation.py      # Ansible playbook and role tests
├── test_integration.py             # Integration tests
├── test_azure_integration.py       # Azure service integration tests
├── test_migration_scenarios.py     # Migration scenario tests
└── README.md                       # This documentation
```

## Prerequisites

- Python 3.8+
- pip
- Azure CLI (for Azure integration tests)
- Terraform (for Terraform validation tests)
- Ansible (for Ansible validation tests)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install additional testing tools:
```bash
# For Terraform compliance testing
pip install terraform-compliance

# For Ansible linting
pip install ansible-lint

# For molecule testing (optional)
pip install molecule[docker]
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories

#### Unit Tests
```bash
# Run all unit tests
pytest -m unit

# Run Terraform-specific unit tests
pytest -m "unit and terraform"

# Run Ansible-specific unit tests
pytest -m "unit and ansible"

# Run Azure-specific unit tests
pytest -m "unit and azure"
```

#### Integration Tests
```bash
# Run all integration tests
pytest -m integration

# Run slow integration tests
pytest -m "integration and slow"
```

#### Mock Tests
```bash
# Run tests using mocks (faster, no external dependencies)
pytest -m mock
```

### Run Specific Test Files
```bash
# Run Terraform validation tests
pytest test_terraform_validation.py

# Run Ansible validation tests
pytest test_ansible_validation.py

# Run integration tests
pytest test_integration.py

# Run Azure integration tests
pytest test_azure_integration.py

# Run migration scenario tests
pytest test_migration_scenarios.py
```

### Run Tests with Coverage
```bash
# Generate coverage report
pytest --cov=../terraform --cov=../ansible --cov-report=html

# View coverage report in browser
open htmlcov/index.html
```

### Run Tests with Different Verbosity
```bash
# Quiet mode
pytest -q

# Verbose mode
pytest -v

# Very verbose mode
pytest -vv
```

## Test Categories and Markers

### Markers
- `unit`: Unit tests that test individual components
- `integration`: Tests that verify component interactions
- `terraform`: Tests related to Terraform configurations
- `ansible`: Tests related to Ansible playbooks and roles
- `azure`: Tests related to Azure service integrations
- `mock`: Tests that use mocks and don't require external services
- `slow`: Tests that take longer to execute

### Test Coverage Areas

#### Terraform Validation Tests (`test_terraform_validation.py`)
- Terraform configuration syntax validation
- Variable validation and type checking
- Resource configuration validation
- Provider configuration testing
- Backend configuration validation
- Output validation
- Security group rule validation
- Virtual network and subnet validation
- Storage account configuration
- Log Analytics workspace setup
- Recovery Services vault configuration
- Backup policy validation
- Monitor action group setup

#### Ansible Validation Tests (`test_ansible_validation.py`)
- Inventory file parsing and validation
- Playbook YAML syntax validation
- Role directory structure validation
- Variable validation and type checking
- Configuration file validation
- Azure collection integration testing
- Error handling pattern validation
- Inventory plugin configuration
- Facts gathering validation

#### Integration Tests (`test_integration.py`)
- End-to-end workflow testing
- Terraform-Ansible integration
- Azure service integration
- Variable consistency validation
- Configuration drift detection
- Migration pipeline orchestration
- Performance and scalability testing
- Error handling and recovery
- Security and compliance validation

#### Azure Integration Tests (`test_azure_integration.py`)
- Azure authentication and authorization
- Resource Group operations
- Virtual Network and Subnet management
- Network Security Group configuration
- Storage Account operations
- Log Analytics workspace management
- Recovery Services vault operations
- Azure Monitor and alerting
- Backup and recovery operations
- Cost management
- Resource tagging
- Resource locks
- Service Health monitoring

#### Migration Scenario Tests (`test_migration_scenarios.py`)
- Single VM migration scenarios
- Multi-VM migration scenarios
- Windows-specific migration scenarios
- Linux-specific migration scenarios
- Database VM migration scenarios
- High availability migration scenarios
- Disaster recovery migration scenarios
- Security-hardened migration scenarios
- Large-scale migration scenarios
- Cloud-native migration scenarios
- Incremental migration approaches
- Rollback procedures
- Cost-optimized migration strategies
- Compliance-focused migration scenarios
- Fully automated migration scenarios
- Migration validation gates

## Test Fixtures

### Shared Fixtures (`conftest.py`)
- `azure_credentials`: Mock Azure authentication credentials
- `subscription_id`: Test Azure subscription ID
- `resource_group_name`: Test resource group name
- `location`: Test Azure location
- `temp_dir`: Temporary directory for test files
- `mock_terraform_config`: Mock Terraform configuration files
- `mock_ansible_inventory`: Mock Ansible inventory file
- `mock_ansible_playbook`: Mock Ansible playbook
- `mock_azure_clients`: Mock Azure management clients
- `sample_terraform_variables`: Sample Terraform variables
- `sample_ansible_variables`: Sample Ansible variables
- `mock_terraform_output`: Mock Terraform outputs
- `mock_ansible_facts`: Mock Ansible facts

## Continuous Integration

### GitHub Actions Integration
The test suite is designed to work with GitHub Actions for CI/CD:

```yaml
- name: Run Tests
  run: |
    pip install -r tests/requirements.txt
    pytest --cov=terraform --cov=ansible --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Pre-commit Hooks
Add the following to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: Run pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## Test Data and Mocking

### Mock Data
The tests use comprehensive mock data to simulate:
- Azure API responses
- Terraform state files
- Ansible facts
- Infrastructure configurations
- Migration scenarios

### Test Data Sources
- Sample Terraform configurations
- Sample Ansible playbooks and inventories
- Mock Azure resource configurations
- Simulated migration scenarios

## Performance Testing

### Benchmarking
```bash
# Run tests with benchmarking
pytest --benchmark-only

# Compare performance over time
pytest --benchmark-autosave --benchmark-compare
```

### Load Testing
```bash
# Run tests in parallel
pytest -n auto

# Run specific slow tests
pytest -m "slow" -v
```

## Debugging Tests

### Debug Failed Tests
```bash
# Run with detailed output
pytest -v --tb=long

# Run specific failing test
pytest test_file.py::TestClass::test_method -v

# Debug with pdb
pytest --pdb
```

### Test Isolation
```bash
# Run tests in isolation
pytest --disable-warnings -q

# Check for test interdependencies
pytest --co -q
```

## Extending the Test Suite

### Adding New Tests
1. Create a new test file following the naming convention `test_*.py`
2. Add appropriate markers and fixtures
3. Follow the existing test structure and patterns
4. Update this README with new test categories

### Adding New Fixtures
1. Add fixtures to `conftest.py`
2. Document the fixture purpose and usage
3. Ensure fixtures are reusable across test files

### Adding New Markers
1. Define new markers in `pytest.ini`
2. Update the markers section in this README
3. Apply markers to relevant tests

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and virtual environment

2. **Azure Authentication Failures**
   - Verify Azure CLI installation and login
   - Check service principal permissions

3. **Terraform Command Not Found**
   - Install Terraform CLI
   - Add Terraform to system PATH

4. **Ansible Command Not Found**
   - Install Ansible
   - Install required Ansible collections

5. **Test Timeouts**
   - Increase timeout values for slow tests
   - Run tests in parallel to reduce execution time

### Getting Help

- Check pytest documentation: https://docs.pytest.org/
- Review Azure SDK documentation
- Consult Terraform and Ansible documentation
- Check existing issues and solutions

## Contributing

1. Follow the existing test structure and naming conventions
2. Add comprehensive docstrings to test methods
3. Include appropriate markers for test categorization
4. Update this README when adding new test categories
5. Ensure tests pass before submitting pull requests

## License

This test suite is part of the Azure VM Migration Pipeline project and follows the same license terms.
