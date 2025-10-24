import pytest
import os
import tempfile
import yaml
import json
from unittest.mock import MagicMock, patch
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient


def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "terraform: Terraform-specific tests")
    config.addinivalue_line("markers", "ansible: Ansible-specific tests")
    config.addinivalue_line("markers", "azure: Azure-related tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "mock: Tests using mocks")


@pytest.fixture(scope="session")
def azure_credentials():
    """Mock Azure credentials for testing."""
    return MagicMock(spec=DefaultAzureCredential)


@pytest.fixture(scope="session")
def subscription_id():
    """Test subscription ID."""
    return "12345678-1234-1234-1234-123456789012"


@pytest.fixture(scope="session")
def resource_group_name():
    """Test resource group name."""
    return "test-migration-rg"


@pytest.fixture(scope="session")
def location():
    """Test Azure location."""
    return "East US"


@pytest.fixture(scope="function")
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture(scope="function")
def mock_terraform_config(temp_dir):
    """Create mock Terraform configuration files."""
    # Create main.tf
    main_tf_content = """
terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "test" {
  name     = "test-rg"
  location = "East US"
}
"""
    with open(os.path.join(temp_dir, "main.tf"), "w") as f:
        f.write(main_tf_content)

    # Create variables.tf
    variables_tf_content = """
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "test"
}

variable "location" {
  description = "Azure location"
  type        = string
  default     = "East US"
}
"""
    with open(os.path.join(temp_dir, "variables.tf"), "w") as f:
        f.write(variables_tf_content)

    # Create terraform.tfvars
    tfvars_content = """
environment = "test"
location     = "East US"
"""
    with open(os.path.join(temp_dir, "terraform.tfvars"), "w") as f:
        f.write(tfvars_content)

    return temp_dir


@pytest.fixture(scope="function")
def mock_ansible_inventory(temp_dir):
    """Create mock Ansible inventory file."""
    inventory_content = """[migrated-vms]
vm1 ansible_host=10.0.1.10 ansible_user=azureuser
vm2 ansible_host=10.0.1.11 ansible_user=azureuser

[migrated-vms:vars]
ansible_ssh_private_key_file=/path/to/key
ansible_python_interpreter=/usr/bin/python3
"""
    inventory_path = os.path.join(temp_dir, "inventory.ini")
    with open(inventory_path, "w") as f:
        f.write(inventory_content)

    return inventory_path


@pytest.fixture(scope="function")
def mock_ansible_playbook(temp_dir):
    """Create mock Ansible playbook."""
    playbook_content = """
---
- name: Test playbook
  hosts: migrated-vms
  become: yes

  tasks:
    - name: Test task
      debug:
        msg: "Hello from test playbook"
"""
    playbook_path = os.path.join(temp_dir, "test.yml")
    with open(playbook_path, "w") as f:
        f.write(playbook_content)

    return playbook_path


@pytest.fixture(scope="function")
def mock_azure_clients(azure_credentials, subscription_id):
    """Mock Azure management clients."""
    with patch('azure.mgmt.resource.ResourceManagementClient') as mock_resource, \
         patch('azure.mgmt.compute.ComputeManagementClient') as mock_compute, \
         patch('azure.mgmt.network.NetworkManagementClient') as mock_network, \
         patch('azure.mgmt.storage.StorageManagementClient') as mock_storage:

        # Configure mock clients
        resource_client = MagicMock(spec=ResourceManagementClient)
        compute_client = MagicMock(spec=ComputeManagementClient)
        network_client = MagicMock(spec=NetworkManagementClient)
        storage_client = MagicMock(spec=StorageManagementClient)

        # Mock network client attributes
        network_client.virtual_networks = MagicMock()
        network_client.subnets = MagicMock()
        network_client.network_security_groups = MagicMock()

        # Mock storage client attributes
        storage_client.storage_accounts = MagicMock()
        storage_client.recovery_services_vaults = MagicMock()
        storage_client.backup_policies = MagicMock()

        # Mock resource client attributes
        resource_client.resource_groups = MagicMock()
        resource_client.subscriptions = MagicMock()
        resource_client.role_assignments = MagicMock()
        resource_client.policy_assignments = MagicMock()
        resource_client.usage_details = MagicMock()
        resource_client.management_locks = MagicMock()
        resource_client.events = MagicMock()

        # Mock compute client attributes (if needed)
        compute_client.virtual_machines = MagicMock()

        # Mock monitor client (for log analytics, alerts)
        from azure.mgmt.monitor import MonitorManagementClient
        with patch('azure.mgmt.monitor.MonitorManagementClient') as mock_monitor:
            monitor_client = MagicMock(spec=MonitorManagementClient)
            monitor_client.workspaces = MagicMock()
            monitor_client.alert_rules = MagicMock()

            yield {
                'resource': resource_client,
                'compute': compute_client,
                'network': network_client,
                'storage': storage_client,
                'monitor': monitor_client
            }


@pytest.fixture(scope="function")
def sample_terraform_variables():
    """Sample Terraform variables for testing."""
    return {
        "environment": "test",
        "location": "East US",
        "vnet_address_space": "10.0.0.0/16",
        "subnet_address_prefix": "10.0.1.0/24",
        "allowed_ip_range": "0.0.0.0/0",
        "storage_account_encryption": True,
        "log_analytics_workspace": True,
        "recovery_vault": True,
        "tags": {
            "Project": "VM Migration",
            "Environment": "test",
            "ManagedBy": "Terraform"
        },
        "vms_to_migrate": [],
        "alert_email": "test@example.com"
    }


@pytest.fixture(scope="function")
def sample_ansible_variables():
    """Sample Ansible variables for testing."""
    return {
        "azure_subscription_id": "12345678-1234-1234-1234-123456789012",
        "resource_group": "test-migration-rg",
        "location": "East US",
        "migration_wave": "wave1",
        "source_environment": "on-premises",
        "target_environment": "azure",
        "app_name": "testapp",
        "app_version": "1.0.0",
        "ssl_enabled": True,
        "azure_access_token": "mock_token",
        "monitoring_enabled": True,
        "backup_configured": True
    }


@pytest.fixture(scope="function")
def mock_terraform_output():
    """Mock Terraform output for testing."""
    return {
        "resource_group_name": {
            "value": "test-migration-rg"
        },
        "vnet_name": {
            "value": "test-vnet"
        },
        "subnet_name": {
            "value": "test-subnet"
        },
        "log_analytics_workspace_id": {
            "value": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/test-migration-rg/providers/Microsoft.OperationalInsights/workspaces/test-logs"
        }
    }


@pytest.fixture(scope="function")
def mock_ansible_facts():
    """Mock Ansible facts for testing."""
    return {
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_version": "20.04",
        "ansible_os_family": "Debian",
        "ansible_architecture": "x86_64",
        "ansible_memtotal_mb": 8192,
        "ansible_processor_count": 2,
        "ansible_default_ipv4": {
            "address": "10.0.1.10",
            "interface": "eth0"
        }
    }
