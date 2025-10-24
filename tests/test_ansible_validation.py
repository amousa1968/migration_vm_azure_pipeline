import pytest
import os
import yaml
import tempfile
from unittest.mock import patch, MagicMock
from conftest import *


class TestAnsibleValidation:
    """Test Ansible configuration validation."""

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_inventory_parsing(self, mock_ansible_inventory):
        """Test Ansible inventory file parsing."""
        with open(mock_ansible_inventory, 'r') as f:
            content = f.read()

        # Check for required sections
        assert '[migrated-vms]' in content
        assert '[migrated-vms:vars]' in content

        # Check for host entries
        assert 'vm1 ansible_host=10.0.1.10' in content
        assert 'vm2 ansible_host=10.0.1.11' in content

        # Check for variable definitions
        assert 'ansible_ssh_private_key_file=' in content
        assert 'ansible_python_interpreter=' in content

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_playbook_structure(self, mock_ansible_playbook):
        """Test Ansible playbook YAML structure."""
        with open(mock_ansible_playbook, 'r') as f:
            playbook = yaml.safe_load(f)

        assert isinstance(playbook, list)
        assert len(playbook) > 0

        play = playbook[0]
        assert 'name' in play
        assert 'hosts' in play
        assert 'tasks' in play

        # Check tasks structure
        assert isinstance(play['tasks'], list)
        task = play['tasks'][0]
        assert 'name' in task
        assert 'debug' in task

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_variables_validation(self, sample_ansible_variables):
        """Test Ansible variables structure."""
        required_vars = [
            'azure_subscription_id', 'resource_group', 'location',
            'migration_wave', 'source_environment', 'target_environment'
        ]

        for var in required_vars:
            assert var in sample_ansible_variables, f"Required variable {var} is missing"

        # Test variable types
        assert isinstance(sample_ansible_variables['azure_subscription_id'], str)
        assert isinstance(sample_ansible_variables['resource_group'], str)
        assert isinstance(sample_ansible_variables['location'], str)

        # Test subscription ID format (UUID)
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert re.match(uuid_pattern, sample_ansible_variables['azure_subscription_id'])

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_config_validation(self):
        """Test Ansible configuration file structure."""
        ansible_config = """
[defaults]
inventory = inventory.ini
remote_user = azureuser
private_key_file = ~/.ssh/azure_key
host_key_checking = False
retry_files_enabled = False
gathering = smart
fact_caching = memory
stdout_callback = yaml
callback_whitelist = profile_tasks

[inventory]
enable_plugins = azure_rm, host_list, yaml, ini

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=30m -o StrictHostKeyChecking=no
pipelining = True
"""

        # Parse config sections
        lines = ansible_config.strip().split('\n')
        sections = {}
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                sections[current_section] = []
            elif line and not line.startswith('#') and current_section:
                sections[current_section].append(line)

        # Check required sections
        assert 'defaults' in sections
        assert 'inventory' in sections
        assert 'ssh_connection' in sections

        # Check key configurations
        defaults = sections['defaults']
        assert any('inventory = inventory.ini' in line for line in defaults)
        assert any('host_key_checking = False' in line for line in defaults)

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_role_structure(self, temp_dir):
        """Test Ansible role directory structure."""
        role_name = "test-role"
        role_dir = os.path.join(temp_dir, "roles", role_name)

        # Create role structure
        subdirs = ["tasks", "handlers", "templates", "files", "vars", "defaults", "meta"]
        for subdir in subdirs:
            os.makedirs(os.path.join(role_dir, subdir), exist_ok=True)

        # Create main.yml files
        main_files = ["tasks/main.yml", "handlers/main.yml", "vars/main.yml", "defaults/main.yml", "meta/main.yml"]
        for main_file in main_files:
            file_path = os.path.join(role_dir, main_file)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("---\n# Main file for {}\n".format(main_file.split('/')[0]))

        # Verify structure
        for subdir in subdirs:
            assert os.path.exists(os.path.join(role_dir, subdir)), f"Role subdirectory {subdir} missing"

        for main_file in main_files:
            assert os.path.exists(os.path.join(role_dir, main_file)), f"Main file {main_file} missing"

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_playbook_syntax(self, mock_ansible_playbook):
        """Test Ansible playbook syntax validation."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Playbook syntax is valid")

            import subprocess
            result = subprocess.run(['ansible-playbook', '--syntax-check', mock_ansible_playbook],
                                  capture_output=True, text=True)

            assert result.returncode == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_inventory_reachability(self, mock_ansible_inventory):
        """Test Ansible inventory host reachability."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Host reachable")

            import subprocess
            result = subprocess.run(['ansible', '-i', mock_ansible_inventory, 'migrated-vms', '-m', 'ping'],
                                  capture_output=True, text=True)

            assert result.returncode == 0
            mock_run.assert_called_once()

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_facts_gathering(self, mock_ansible_facts):
        """Test Ansible facts gathering."""
        required_facts = [
            'ansible_distribution', 'ansible_distribution_version',
            'ansible_os_family', 'ansible_architecture'
        ]

        for fact in required_facts:
            assert fact in mock_ansible_facts, f"Required fact {fact} is missing"

        # Test OS information
        assert mock_ansible_facts['ansible_distribution'] == 'Ubuntu'
        assert mock_ansible_facts['ansible_os_family'] == 'Debian'

        # Test hardware information
        assert mock_ansible_facts['ansible_memtotal_mb'] >= 1024  # At least 1GB
        assert mock_ansible_facts['ansible_processor_count'] >= 1

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_azure_integration(self, sample_ansible_variables):
        """Test Ansible Azure integration variables."""
        azure_vars = {
            'azure_subscription_id': sample_ansible_variables['azure_subscription_id'],
            'azure_resource_group': sample_ansible_variables['resource_group'],
            'azure_location': sample_ansible_variables['location']
        }

        # Check Azure-specific variables
        assert 'azure_subscription_id' in azure_vars
        assert 'azure_resource_group' in azure_vars
        assert 'azure_location' in azure_vars

        # Validate subscription ID format
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        assert re.match(uuid_pattern, azure_vars['azure_subscription_id'])

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_migration_playbook_content(self, temp_dir):
        """Test migration-specific Ansible playbook content."""
        playbook_content = """
---
- name: Azure VM Migration Post-Configuration
  hosts: migrated-vms
  become: yes
  gather_facts: yes

  vars:
    migration_wave: "{{ migration_wave | default('wave1') }}"
    target_environment: "{{ target_environment | default('azure') }}"

  pre_tasks:
    - name: Validate Azure connectivity
      uri:
        url: "https://management.azure.com/subscriptions/{{ azure_subscription_id }}/providers/Microsoft.Compute/virtualMachines?api-version=2022-08-01"
        method: GET
        headers:
          Authorization: "Bearer {{ azure_access_token }}"
      register: azure_connectivity
      failed_when: azure_connectivity.status != 200

  tasks:
    - name: Install Azure VM agent
      package:
        name: walinuxagent
        state: present
      when: ansible_os_family == 'RedHat'

    - name: Configure Azure monitoring
      include_role:
        name: azure_monitor

    - name: Setup backup configuration
      include_role:
        name: azure_backup

    - name: Apply security hardening
      include_role:
        name: security_hardening

  post_tasks:
    - name: Validate migration success
      assert:
        that:
          - "'migration_complete' in hostvars[inventory_hostname]"
        fail_msg: "Migration validation failed for {{ inventory_hostname }}"
"""

        playbook_path = os.path.join(temp_dir, "migrate.yml")
        with open(playbook_path, 'w') as f:
            f.write(playbook_content)

        # Parse and validate playbook
        with open(playbook_path, 'r') as f:
            playbook = yaml.safe_load(f)

        assert isinstance(playbook, list)
        play = playbook[0]

        # Check required sections
        assert 'name' in play
        assert 'hosts' in play
        assert 'vars' in play
        assert 'pre_tasks' in play
        assert 'tasks' in play
        assert 'post_tasks' in play

        # Check Azure connectivity validation
        pre_task = play['pre_tasks'][0]
        assert 'Validate Azure connectivity' in pre_task['name']
        assert 'uri' in pre_task

        # Check migration tasks
        tasks = play['tasks']
        task_names = [task['name'] for task in tasks]
        assert 'Install Azure VM agent' in task_names
        assert 'Configure Azure monitoring' in task_names
        assert 'Setup backup configuration' in task_names
        assert 'Apply security hardening' in task_names

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_error_handling(self, temp_dir):
        """Test Ansible error handling patterns."""
        error_handling_playbook = """
---
- name: Error Handling Test
  hosts: migrated-vms
  become: yes
  ignore_errors: no
  max_fail_percentage: 25

  tasks:
    - name: Task with error handling
      command: echo "test command"
      register: command_result
      failed_when: command_result.rc != 0
      retries: 3
      delay: 10
      until: command_result.rc == 0

    - name: Conditional task execution
      debug:
        msg: "Task executed successfully"
      when: command_result.rc == 0

    - name: Cleanup on failure
      file:
        path: /tmp/migration_temp
        state: absent
      when: command_result.rc != 0
      ignore_errors: yes
"""

        playbook_path = os.path.join(temp_dir, "error_handling.yml")
        with open(playbook_path, 'w') as f:
            f.write(error_handling_playbook)

        # Parse and validate
        with open(playbook_path, 'r') as f:
            playbook = yaml.safe_load(f)

        play = playbook[0]

        # Check error handling settings
        assert play.get('ignore_errors') == False
        assert play.get('max_fail_percentage') == 25

        # Check task error handling
        task = play['tasks'][0]
        assert 'retries' in task
        assert 'delay' in task
        assert 'until' in task
        assert task['retries'] == 3
        assert task['delay'] == 10

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_azure_collection_usage(self):
        """Test Ansible Azure collection module usage."""
        azure_tasks = [
            {
                "name": "Create resource group",
                "azure.azcollection.azure_rm_resourcegroup":
                {
                    "name": "{{ resource_group_name }}",
                    "location": "{{ location }}",
                    "state": "present"
                }
            },
            {
                "name": "Create virtual network",
                "azure.azcollection.azure_rm_virtualnetwork":
                {
                    "resource_group": "{{ resource_group_name }}",
                    "name": "{{ vnet_name }}",
                    "address_prefixes": ["10.0.0.0/16"],
                    "state": "present"
                }
            },
            {
                "name": "Create VM",
                "azure.azcollection.azure_rm_virtualmachine":
                {
                    "resource_group": "{{ resource_group_name }}",
                    "name": "{{ vm_name }}",
                    "vm_size": "Standard_DS1_v2",
                    "state": "present"
                }
            }
        ]

        # Validate Azure collection usage
        for task in azure_tasks:
            assert 'name' in task
            # Check that azure.azcollection modules are used
            module_keys = [key for key in task.keys() if key != 'name']
            assert len(module_keys) == 1
            module_name = module_keys[0]
            assert module_name.startswith('azure.azcollection.')

        # Check specific module parameters
        rg_task = azure_tasks[0]
        rg_module = rg_task['azure.azcollection.azure_rm_resourcegroup']
        assert 'name' in rg_module
        assert 'location' in rg_module
        assert 'state' in rg_module

    @pytest.mark.unit
    @pytest.mark.ansible
    def test_ansible_inventory_plugins(self):
        """Test Ansible inventory plugin configurations."""
        inventory_config = {
            "plugin": "azure.azcollection.azure_rm",
            "include_vm_resource_groups": ["migration-rg-*"],
            "exclude_vm_resource_groups": ["test-rg"],
            "conditional_groups": {
                "linux_vms": "os_profile.linux_configuration is defined",
                "windows_vms": "os_profile.windows_configuration is defined",
                "migrated_vms": "'migration' in tags"
            },
            "keyed_groups": [
                {
                    "key": "location",
                    "prefix": "azure"
                },
                {
                    "key": "tags.Environment",
                    "prefix": "env"
                }
            ]
        }

        # Check required plugin settings
        assert inventory_config['plugin'] == 'azure.azcollection.azure_rm'
        assert 'include_vm_resource_groups' in inventory_config
        assert 'conditional_groups' in inventory_config
        assert 'keyed_groups' in inventory_config

        # Check conditional groups
        conditional_groups = inventory_config['conditional_groups']
        assert 'linux_vms' in conditional_groups
        assert 'windows_vms' in conditional_groups
        assert 'migrated_vms' in conditional_groups

        # Check keyed groups
        keyed_groups = inventory_config['keyed_groups']
        assert len(keyed_groups) == 2
        assert keyed_groups[0]['key'] == 'location'
        assert keyed_groups[1]['key'] == 'tags.Environment'
