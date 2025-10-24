import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from conftest import *
from azure.core.exceptions import ServiceRequestError, ResourceNotFoundError


class TestAzureIntegration:
    """Test Azure service integration."""

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_authentication(self, azure_credentials, subscription_id):
        """Test Azure authentication setup."""
        with patch('azure.identity.DefaultAzureCredential') as mock_cred:
            mock_cred.return_value = azure_credentials

            # Simulate authentication
            credential = mock_cred()
            token = credential.get_token("https://management.azure.com/.default")

            assert credential is not None
            assert token is not None

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_resource_group_operations(self, mock_azure_clients, subscription_id, resource_group_name, location):
        """Test Azure Resource Group operations."""
        clients = mock_azure_clients

        # Mock successful creation
        clients['resource'].resource_groups.create_or_update.return_value = {
            'name': resource_group_name,
            'location': location,
            'tags': {}
        }

        # Test creation
        rg_params = {
            'location': location,
            'tags': {'Environment': 'test'}
        }

        result = clients['resource'].resource_groups.create_or_update(
            resource_group_name, rg_params
        )

        assert result['name'] == resource_group_name
        assert result['location'] == location

        # Test retrieval
        clients['resource'].resource_groups.get.return_value = result
        retrieved = clients['resource'].resource_groups.get(resource_group_name)

        assert retrieved['name'] == resource_group_name

        # Test deletion
        clients['resource'].resource_groups.delete.return_value = None
        clients['resource'].resource_groups.delete(resource_group_name)

        clients['resource'].resource_groups.delete.assert_called_once_with(resource_group_name)

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_virtual_network_operations(self, mock_azure_clients, resource_group_name, location):
        """Test Azure Virtual Network operations."""
        clients = mock_azure_clients

        vnet_name = 'test-vnet'
        vnet_params = {
            'location': location,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }

        # Mock creation
        clients['network'].virtual_networks.create_or_update.return_value = {
            'name': vnet_name,
            'address_space': {'address_prefixes': ['10.0.0.0/16']},
            'location': location
        }

        result = clients['network'].virtual_networks.create_or_update(
            resource_group_name, vnet_name, vnet_params
        )

        assert result['name'] == vnet_name
        assert '10.0.0.0/16' in result['address_space']['address_prefixes']

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_subnet_operations(self, mock_azure_clients, resource_group_name):
        """Test Azure Subnet operations."""
        clients = mock_azure_clients

        vnet_name = 'test-vnet'
        subnet_name = 'test-subnet'
        subnet_params = {
            'address_prefix': '10.0.1.0/24'
        }

        # Mock creation
        clients['network'].subnets.create_or_update.return_value = {
            'name': subnet_name,
            'address_prefix': '10.0.1.0/24'
        }

        result = clients['network'].subnets.create_or_update(
            resource_group_name, vnet_name, subnet_name, subnet_params
        )

        assert result['name'] == subnet_name
        assert result['address_prefix'] == '10.0.1.0/24'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_nsg_operations(self, mock_azure_clients, resource_group_name, location):
        """Test Azure Network Security Group operations."""
        clients = mock_azure_clients

        nsg_name = 'test-nsg'
        nsg_params = {
            'location': location,
            'security_rules': [
                {
                    'name': 'allow-rdp',
                    'properties': {
                        'priority': 100,
                        'direction': 'Inbound',
                        'access': 'Allow',
                        'protocol': 'Tcp',
                        'source_port_range': '*',
                        'destination_port_range': '3389',
                        'source_address_prefix': '*',
                        'destination_address_prefix': '*'
                    }
                }
            ]
        }

        # Mock creation
        clients['network'].network_security_groups.create_or_update.return_value = {
            'name': nsg_name,
            'location': location,
            'security_rules': nsg_params['security_rules']
        }

        result = clients['network'].network_security_groups.create_or_update(
            resource_group_name, nsg_name, nsg_params
        )

        assert result['name'] == nsg_name
        assert len(result['security_rules']) == 1
        assert result['security_rules'][0]['name'] == 'allow-rdp'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_storage_account_operations(self, mock_azure_clients, resource_group_name, location):
        """Test Azure Storage Account operations."""
        clients = mock_azure_clients

        storage_name = 'teststorage123'
        storage_params = {
            'location': location,
            'sku': {'name': 'Standard_LRS'},
            'kind': 'StorageV2',
            'properties': {
                'supports_https_traffic_only': True,
                'encryption': {
                    'services': {
                        'blob': {'enabled': True}
                    },
                    'key_source': 'Microsoft.Storage'
                }
            }
        }

        # Mock creation
        clients['storage'].storage_accounts.create.return_value = {
            'name': storage_name,
            'location': location,
            'sku': {'name': 'Standard_LRS'}
        }

        result = clients['storage'].storage_accounts.create(
            resource_group_name, storage_name, storage_params
        )

        assert result['name'] == storage_name
        assert result['sku']['name'] == 'Standard_LRS'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_log_analytics_operations(self, mock_azure_clients, resource_group_name, location):
        """Test Azure Log Analytics operations."""
        clients = mock_azure_clients

        workspace_name = 'test-log-analytics'
        workspace_params = {
            'location': location,
            'properties': {
                'sku': {'name': 'PerGB2018'},
                'retention_in_days': 30
            }
        }

        # Mock creation
        clients['monitor'].workspaces.create_or_update.return_value = {
            'name': workspace_name,
            'location': location,
            'sku': {'name': 'PerGB2018'},
            'retention_in_days': 30
        }

        # Note: Using monitor client for Log Analytics
        result = clients['monitor'].workspaces.create_or_update(
            resource_group_name, workspace_name, workspace_params
        )

        assert result['name'] == workspace_name
        assert result['sku']['name'] == 'PerGB2018'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_recovery_services_operations(self, mock_azure_clients, resource_group_name, location):
        """Test Azure Recovery Services operations."""
        clients = mock_azure_clients

        vault_name = 'test-recovery-vault'
        vault_params = {
            'location': location,
            'sku': {'name': 'Standard'},
            'properties': {}
        }

        # Mock creation
        clients['storage'].recovery_services_vaults.create_or_update.return_value = {
            'name': vault_name,
            'location': location,
            'sku': {'name': 'Standard'}
        }

        result = clients['storage'].recovery_services_vaults.create_or_update(
            resource_group_name, vault_name, vault_params
        )

        assert result['name'] == vault_name
        assert result['sku']['name'] == 'Standard'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_error_handling(self, mock_azure_clients, resource_group_name):
        """Test Azure API error handling."""
        clients = mock_azure_clients

        # Test resource not found
        clients['resource'].resource_groups.get.side_effect = ResourceNotFoundError("Resource not found")

        with pytest.raises(ResourceNotFoundError):
            clients['resource'].resource_groups.get(resource_group_name)

        # Test service request error
        clients['resource'].resource_groups.create_or_update.side_effect = ServiceRequestError("Service error")

        with pytest.raises(ServiceRequestError):
            clients['resource'].resource_groups.create_or_update(resource_group_name, {})

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_subscription_info(self, mock_azure_clients, subscription_id):
        """Test Azure subscription information retrieval."""
        clients = mock_azure_clients

        subscription_info = {
            'subscription_id': subscription_id,
            'display_name': 'Test Subscription',
            'state': 'Enabled',
            'location_placement_id': 'test-location'
        }

        clients['resource'].subscriptions.get.return_value = subscription_info

        result = clients['resource'].subscriptions.get(subscription_id)

        assert result['subscription_id'] == subscription_id
        assert result['state'] == 'Enabled'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_resource_providers(self, mock_azure_clients, subscription_id):
        """Test Azure resource provider operations."""
        clients = mock_azure_clients

        providers = [
            {'namespace': 'Microsoft.Compute', 'registration_state': 'Registered'},
            {'namespace': 'Microsoft.Network', 'registration_state': 'Registered'},
            {'namespace': 'Microsoft.Storage', 'registration_state': 'Registered'}
        ]

        clients['resource'].providers.list.return_value = providers

        result = list(clients['resource'].providers.list())

        assert len(result) == 3
        namespaces = [p['namespace'] for p in result]
        assert 'Microsoft.Compute' in namespaces
        assert 'Microsoft.Network' in namespaces
        assert 'Microsoft.Storage' in namespaces

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_role_assignments(self, mock_azure_clients, subscription_id):
        """Test Azure role assignment operations."""
        clients = mock_azure_clients

        role_assignment = {
            'id': f'/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleAssignments/test-id',
            'properties': {
                'principal_id': 'test-principal-id',
                'role_definition_id': '/subscriptions/test/providers/Microsoft.Authorization/roleDefinitions/test-role',
                'scope': f'/subscriptions/{subscription_id}'
            }
        }

        clients['resource'].role_assignments.create.return_value = role_assignment

        result = clients['resource'].role_assignments.create(
            scope=f'/subscriptions/{subscription_id}',
            role_assignment_name='test-assignment',
            parameters={
                'properties': {
                    'principal_id': 'test-principal-id',
                    'role_definition_id': '/subscriptions/test/providers/Microsoft.Authorization/roleDefinitions/test-role'
                }
            }
        )

        assert result['properties']['principal_id'] == 'test-principal-id'
        assert subscription_id in result['id']

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_policy_assignments(self, mock_azure_clients, subscription_id):
        """Test Azure policy assignment operations."""
        clients = mock_azure_clients

        policy_assignment = {
            'name': 'test-policy-assignment',
            'properties': {
                'policy_definition_id': '/providers/Microsoft.Authorization/policyDefinitions/test-policy',
                'scope': f'/subscriptions/{subscription_id}',
                'parameters': {}
            }
        }

        clients['resource'].policy_assignments.create.return_value = policy_assignment

        result = clients['resource'].policy_assignments.create(
            scope=f'/subscriptions/{subscription_id}',
            policy_assignment_name='test-policy-assignment',
            parameters=policy_assignment
        )

        assert result['name'] == 'test-policy-assignment'
        assert 'policy_definition_id' in result['properties']

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_monitor_alerts(self, mock_azure_clients, resource_group_name):
        """Test Azure Monitor alert operations."""
        clients = mock_azure_clients

        alert_rule = {
            'location': 'Global',
            'properties': {
                'description': 'Test alert rule',
                'enabled': True,
                'condition': {
                    'odata.type': 'Microsoft.Azure.Management.Insights.Models.ThresholdRuleCondition',
                    'operator': 'GreaterThan',
                    'threshold': 80,
                    'window_size': 'PT5M'
                },
                'actions': []
            }
        }

        clients['monitor'].alert_rules.create_or_update.return_value = alert_rule

        result = clients['monitor'].alert_rules.create_or_update(
            resource_group_name, 'test-alert-rule', alert_rule
        )

        assert result['properties']['enabled'] == True
        assert result['properties']['condition']['operator'] == 'GreaterThan'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_backup_operations(self, mock_azure_clients, resource_group_name):
        """Test Azure Backup operations."""
        clients = mock_azure_clients

        vault_name = 'test-backup-vault'
        backup_policy = {
            'properties': {
                'backup_management_type': 'AzureIaasVM',
                'schedule_policy': {
                    'schedule_run_frequency': 'Daily',
                    'schedule_run_times': ['2023-01-01T02:00:00Z']
                },
                'retention_policy': {
                    'daily_schedule': {
                        'retention_times': ['2023-01-01T02:00:00Z'],
                        'retention_duration': {'count': 30, 'duration_type': 'Days'}
                    }
                }
            }
        }

        clients['storage'].backup_policies.create_or_update.return_value = backup_policy

        result = clients['storage'].backup_policies.create_or_update(
            resource_group_name, vault_name, 'test-policy', backup_policy
        )

        assert result['properties']['backup_management_type'] == 'AzureIaasVM'
        assert result['properties']['schedule_policy']['schedule_run_frequency'] == 'Daily'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_cost_management(self, mock_azure_clients, subscription_id):
        """Test Azure Cost Management operations."""
        clients = mock_azure_clients

        cost_data = {
            'properties': {
                'next_link': None,
                'columns': [
                    {'name': 'PreTaxCost', 'type': 'Number'},
                    {'name': 'Currency', 'type': 'String'}
                ],
                'rows': [
                    [100.50, 'USD'],
                    [75.25, 'USD']
                ]
            }
        }

        clients['resource'].usage_details.list.return_value = [cost_data]

        result = list(clients['resource'].usage_details.list(
            scope=f'/subscriptions/{subscription_id}'
        ))

        assert len(result) == 1
        assert result[0]['properties']['rows'][0][1] == 'USD'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_tags_operations(self, mock_azure_clients, resource_group_name):
        """Test Azure resource tagging operations."""
        clients = mock_azure_clients

        tags = {
            'Environment': 'test',
            'Project': 'VM Migration',
            'Owner': 'test-team'
        }

        # Mock tagging operation
        clients['resource'].tags.create_or_update_at_scope.return_value = tags

        result = clients['resource'].tags.create_or_update_at_scope(
            scope=f'/subscriptions/test/resourceGroups/{resource_group_name}',
            parameters={'properties': {'tags': tags}}
        )

        assert result['Environment'] == 'test'
        assert result['Project'] == 'VM Migration'
        assert result['Owner'] == 'test-team'

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_resource_locks(self, mock_azure_clients, resource_group_name):
        """Test Azure resource lock operations."""
        clients = mock_azure_clients

        lock = {
            'properties': {
                'level': 'CanNotDelete',
                'notes': 'Prevent accidental deletion of migration resources'
            }
        }

        clients['resource'].management_locks.create_or_update_at_resource_group_level.return_value = lock

        result = clients['resource'].management_locks.create_or_update_at_resource_group_level(
            resource_group_name, 'migration-lock', lock
        )

        assert result['properties']['level'] == 'CanNotDelete'
        assert 'migration' in result['properties']['notes']

    @pytest.mark.unit
    @pytest.mark.azure
    def test_azure_service_health(self, mock_azure_clients, subscription_id):
        """Test Azure Service Health operations."""
        clients = mock_azure_clients

        health_events = [
            {
                'name': 'test-event',
                'properties': {
                    'title': 'Service maintenance',
                    'description': 'Planned maintenance',
                    'event_type': 'ServiceIssue',
                    'status': 'Active'
                }
            }
        ]

        clients['resource'].events.list.return_value = health_events

        result = list(clients['resource'].events.list(
            scope=f'/subscriptions/{subscription_id}'
        ))

        assert len(result) == 1
        assert result[0]['properties']['event_type'] == 'ServiceIssue'
        assert result[0]['properties']['status'] == 'Active'
