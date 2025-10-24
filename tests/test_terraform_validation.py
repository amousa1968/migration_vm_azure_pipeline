import pytest
import os
import subprocess
import json
from unittest.mock import patch, MagicMock
from conftest import *


class TestTerraformValidation:
    """Test Terraform configuration validation."""

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_init(self, mock_terraform_config, temp_dir):
        """Test Terraform initialization."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Terraform initialized successfully")

            # Change to terraform directory
            terraform_dir = os.path.join(os.path.dirname(mock_terraform_config), "terraform")
            os.makedirs(terraform_dir, exist_ok=True)

            # Copy config files to terraform dir
            for file in os.listdir(mock_terraform_config):
                src = os.path.join(mock_terraform_config, file)
                dst = os.path.join(terraform_dir, file)
                with open(src, 'r') as f_src, open(dst, 'w') as f_dst:
                    f_dst.write(f_src.read())

            # Run terraform init
            result = subprocess.run(['terraform', 'init'], cwd=terraform_dir, capture_output=True, text=True)

            assert result.returncode == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_validate(self, mock_terraform_config):
        """Test Terraform configuration validation."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Configuration is valid")

            result = subprocess.run(['terraform', 'validate'], cwd=mock_terraform_config, capture_output=True, text=True)

            assert result.returncode == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_plan(self, mock_terraform_config):
        """Test Terraform plan generation."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Plan generated successfully")

            result = subprocess.run(['terraform', 'plan', '-no-color'], cwd=mock_terraform_config, capture_output=True, text=True)

            assert result.returncode == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_variables_validation(self, sample_terraform_variables):
        """Test Terraform variables structure."""
        required_vars = [
            'environment', 'location', 'vnet_address_space',
            'subnet_address_prefix', 'allowed_ip_range', 'tags'
        ]

        for var in required_vars:
            assert var in sample_terraform_variables, f"Required variable {var} is missing"

        # Test variable types
        assert isinstance(sample_terraform_variables['environment'], str)
        assert isinstance(sample_terraform_variables['location'], str)
        assert isinstance(sample_terraform_variables['tags'], dict)

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_outputs_structure(self, mock_terraform_output):
        """Test Terraform outputs structure."""
        expected_outputs = [
            'resource_group_name', 'vnet_name', 'subnet_name', 'log_analytics_workspace_id'
        ]

        for output in expected_outputs:
            assert output in mock_terraform_output, f"Required output {output} is missing"
            assert 'value' in mock_terraform_output[output], f"Output {output} missing value key"

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_provider_configuration(self):
        """Test Terraform provider configuration."""
        provider_config = {
            "azurerm": {
                "source": "hashicorp/azurerm",
                "version": "~> 3.0"
            },
            "azuread": {
                "source": "hashicorp/azuread",
                "version": "~> 2.0"
            },
            "random": {
                "source": "hashicorp/random",
                "version": "~> 3.0"
            }
        }

        # Check required providers
        assert "azurerm" in provider_config
        assert "azuread" in provider_config
        assert "random" in provider_config

        # Check version constraints
        assert "~> 3.0" in provider_config["azurerm"]["version"]
        assert "~> 2.0" in provider_config["azuread"]["version"]
        assert "~> 3.0" in provider_config["random"]["version"]

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_backend_configuration(self):
        """Test Terraform backend configuration."""
        backend_config = {
            "resource_group_name": "tfstate-rg",
            "storage_account_name": "tfstatestorage",
            "container_name": "tfstate",
            "key": "terraform.tfstate"
        }

        required_keys = ["resource_group_name", "storage_account_name", "container_name", "key"]

        for key in required_keys:
            assert key in backend_config, f"Backend configuration missing {key}"

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_resource_group_creation(self, sample_terraform_variables):
        """Test resource group resource configuration."""
        rg_config = {
            "name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "location": sample_terraform_variables['location'],
            "tags": sample_terraform_variables['tags']
        }

        assert rg_config['name'].startswith('migration-isolation-zone-')
        assert rg_config['location'] == sample_terraform_variables['location']
        assert rg_config['tags'] == sample_terraform_variables['tags']

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_network_security_group(self, sample_terraform_variables):
        """Test NSG configuration."""
        nsg_config = {
            "name": f"migration-nsg-{sample_terraform_variables['environment']}",
            "location": sample_terraform_variables['location'],
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "tags": sample_terraform_variables['tags']
        }

        assert nsg_config['name'].startswith('migration-nsg-')
        assert nsg_config['location'] == sample_terraform_variables['location']

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_security_rules(self, sample_terraform_variables):
        """Test NSG security rules."""
        security_rules = [
            {
                "name": "allow-rdp",
                "priority": 100,
                "direction": "Inbound",
                "access": "Allow",
                "protocol": "Tcp",
                "source_port_range": "*",
                "destination_port_range": "3389",
                "source_address_prefix": sample_terraform_variables['allowed_ip_range'],
                "destination_address_prefix": "*"
            },
            {
                "name": "allow-ssh",
                "priority": 110,
                "direction": "Inbound",
                "access": "Allow",
                "protocol": "Tcp",
                "source_port_range": "*",
                "destination_port_range": "22",
                "source_address_prefix": sample_terraform_variables['allowed_ip_range'],
                "destination_address_prefix": "*"
            }
        ]

        # Test RDP rule
        rdp_rule = security_rules[0]
        assert rdp_rule['name'] == 'allow-rdp'
        assert rdp_rule['destination_port_range'] == '3389'
        assert rdp_rule['source_address_prefix'] == sample_terraform_variables['allowed_ip_range']

        # Test SSH rule
        ssh_rule = security_rules[1]
        assert ssh_rule['name'] == 'allow-ssh'
        assert ssh_rule['destination_port_range'] == '22'
        assert ssh_rule['source_address_prefix'] == sample_terraform_variables['allowed_ip_range']

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_virtual_network(self, sample_terraform_variables):
        """Test virtual network configuration."""
        vnet_config = {
            "name": f"migration-vnet-{sample_terraform_variables['environment']}",
            "location": sample_terraform_variables['location'],
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "address_space": [sample_terraform_variables['vnet_address_space']],
            "tags": sample_terraform_variables['tags']
        }

        assert vnet_config['name'].startswith('migration-vnet-')
        assert vnet_config['address_space'] == [sample_terraform_variables['vnet_address_space']]

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_subnet(self, sample_terraform_variables):
        """Test subnet configuration."""
        subnet_config = {
            "name": f"migration-subnet-{sample_terraform_variables['environment']}",
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "virtual_network_name": f"migration-vnet-{sample_terraform_variables['environment']}",
            "address_prefixes": [sample_terraform_variables['subnet_address_prefix']]
        }

        assert subnet_config['name'].startswith('migration-subnet-')
        assert subnet_config['address_prefixes'] == [sample_terraform_variables['subnet_address_prefix']]

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_storage_account(self, sample_terraform_variables):
        """Test storage account configuration."""
        storage_config = {
            "name": f"migrationdiag{sample_terraform_variables['environment']}random",
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "location": sample_terraform_variables['location'],
            "account_tier": "Standard",
            "account_replication_type": "LRS",
            "tags": sample_terraform_variables['tags']
        }

        assert storage_config['name'].startswith('migrationdiag')
        assert storage_config['account_tier'] == 'Standard'
        assert storage_config['account_replication_type'] == 'LRS'

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_log_analytics_workspace(self, sample_terraform_variables):
        """Test Log Analytics workspace configuration."""
        la_config = {
            "name": f"migration-logs-{sample_terraform_variables['environment']}",
            "location": sample_terraform_variables['location'],
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "sku": "PerGB2018",
            "retention_in_days": 30,
            "tags": sample_terraform_variables['tags']
        }

        assert la_config['name'].startswith('migration-logs-')
        assert la_config['sku'] == 'PerGB2018'
        assert la_config['retention_in_days'] == 30

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_recovery_services_vault(self, sample_terraform_variables):
        """Test Recovery Services vault configuration."""
        vault_config = {
            "name": f"migration-vault-{sample_terraform_variables['environment']}",
            "location": sample_terraform_variables['location'],
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "sku": "Standard",
            "tags": sample_terraform_variables['tags']
        }

        assert vault_config['name'].startswith('migration-vault-')
        assert vault_config['sku'] == 'Standard'

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_backup_policy(self, sample_terraform_variables):
        """Test backup policy configuration."""
        policy_config = {
            "name": f"migration-backup-policy-{sample_terraform_variables['environment']}",
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "recovery_vault_name": f"migration-vault-{sample_terraform_variables['environment']}",
            "backup": {
                "frequency": "Daily",
                "time": "23:00"
            },
            "retention_daily": {
                "count": 30
            },
            "retention_weekly": {
                "count": 12,
                "weekdays": ["Sunday"]
            }
        }

        assert policy_config['name'].startswith('migration-backup-policy-')
        assert policy_config['backup']['frequency'] == 'Daily'
        assert policy_config['backup']['time'] == '23:00'
        assert policy_config['retention_daily']['count'] == 30
        assert policy_config['retention_weekly']['count'] == 12

    @pytest.mark.unit
    @pytest.mark.terraform
    def test_terraform_monitor_action_group(self, sample_terraform_variables):
        """Test monitor action group configuration."""
        ag_config = {
            "name": f"critical-alerts-{sample_terraform_variables['environment']}",
            "resource_group_name": f"migration-isolation-zone-{sample_terraform_variables['environment']}",
            "short_name": "critical",
            "email_receiver": {
                "name": "admin",
                "email_address": sample_terraform_variables['alert_email']
            }
        }

        assert ag_config['name'].startswith('critical-alerts-')
        assert ag_config['short_name'] == 'critical'
        assert ag_config['email_receiver']['email_address'] == sample_terraform_variables['alert_email']
