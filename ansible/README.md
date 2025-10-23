# Azure VM Migration Pipeline - Ansible Automation

This Ansible project automates the post-migration configuration and setup of Azure Virtual Machines that have been migrated using Azure Migrate or similar tools. It handles the final configuration steps to ensure migrated VMs are properly integrated into the target Azure environment.

## Overview

The Ansible automation focuses on:
- Post-migration VM configuration
- Application deployment and setup
- Network configuration validation
- Security hardening
- Monitoring agent installation
- Backup configuration verification

## Directory Structure

```
ansible/
├── README.md                    # This documentation
├── ansible.cfg                  # Ansible configuration
├── inventory/                   # Dynamic inventory scripts
├── playbooks/                   # Main playbooks
│   ├── post-migration.yml       # Main post-migration playbook
│   ├── app-deployment.yml       # Application deployment
│   ├── monitoring-setup.yml     # Monitoring configuration
│   └── security-hardening.yml   # Security configurations
├── roles/                       # Ansible roles
│   ├── azure-vm-config/         # Azure VM specific configurations
│   ├── app-deployment/          # Application deployment logic
│   ├── monitoring/              # Monitoring setup (Azure Monitor, etc.)
│   ├── security/                # Security hardening
│   └── networking/              # Network configuration
├── group_vars/                  # Group variables
│   ├── all.yml                  # Global variables
│   ├── migrated-vms.yml         # Variables for migrated VMs
│   └── target-environment.yml   # Target environment variables
├── host_vars/                   # Host-specific variables
├── files/                       # Static files and templates
│   ├── scripts/                 # Utility scripts
│   └── configs/                 # Configuration files
├── templates/                   # Jinja2 templates
└── vars/                        # Additional variables
```

## Prerequisites

- Ansible 2.9+
- Azure CLI installed and authenticated (`az login`)
- SSH access to migrated VMs
- Python 3 on target VMs
- Azure subscription with appropriate permissions

## Usage

### 1. Configure Inventory

The inventory can be dynamic, pulling from Azure Resource Manager:

```bash
# Using Azure RM inventory plugin
ansible-inventory -i azure_rm.yml --list
```

Or static inventory in `inventory/hosts`:

```ini
[migrated-vms]
vm1 ansible_host=10.0.1.10
vm2 ansible_host=10.0.1.11

[migrated-vms:vars]
ansible_user=azureuser
ansible_ssh_private_key_file=~/.ssh/azure_key
```

### 2. Configure Variables

Edit `group_vars/all.yml` for global settings:

```yaml
azure_subscription_id: "your-subscription-id"
resource_group: "migration-target-rg"
location: "East US"
environment: "prod"
```

### 3. Run Post-Migration Setup

Execute the main post-migration playbook:

```bash
ansible-playbook -i inventory/ playbooks/post-migration.yml
```

### 4. Deploy Applications

Deploy applications to migrated VMs:

```bash
ansible-playbook -i inventory/ playbooks/app-deployment.yml
```

### 5. Setup Monitoring

Configure monitoring and alerting:

```bash
ansible-playbook -i inventory/ playbooks/monitoring-setup.yml
```

## Roles Description

### azure-vm-config
- Configures Azure VM extensions
- Sets up Azure VM agent
- Configures Azure-specific settings
- Validates VM migration status

### app-deployment
- Deploys applications to migrated VMs
- Configures application settings
- Sets up application dependencies
- Validates application functionality

### monitoring
- Installs Azure Monitor agent
- Configures Log Analytics workspace
- Sets up Azure Monitor alerts
- Configures application insights

### security
- Applies Azure security baselines
- Configures Azure Security Center
- Sets up network security groups
- Implements Azure Policy compliance

### networking
- Validates network connectivity
- Configures DNS settings
- Sets up load balancers
- Configures Azure Firewall rules

## Key Playbooks

### post-migration.yml
Main playbook that orchestrates the complete post-migration process:
- VM configuration validation
- Network setup verification
- Security hardening
- Basic monitoring setup

### app-deployment.yml
Handles application-specific deployments:
- Database migrations
- Application configuration
- Service dependencies
- Health checks

### monitoring-setup.yml
Comprehensive monitoring configuration:
- Azure Monitor setup
- Log Analytics integration
- Alert configuration
- Dashboard setup

### security-hardening.yml
Security-focused configurations:
- Azure Security Center integration
- Compliance checks
- Vulnerability assessments
- Access control setup

## Variables

### Global Variables (group_vars/all.yml)
```yaml
# Azure settings
azure_subscription_id: "xxx-xxx-xxx"
resource_group: "migration-rg"
location: "East US"

# Migration settings
migration_wave: "wave1"
source_environment: "on-premises"
target_environment: "azure"

# Application settings
app_name: "myapp"
app_version: "1.0.0"
```

### VM-Specific Variables (host_vars/)
```yaml
# vm1.yml
vm_name: "web-server-01"
private_ip: "10.0.1.10"
app_role: "web"
backup_schedule: "daily"
monitoring_level: "detailed"
```

## Security Considerations

- Use Azure Key Vault for sensitive data
- Implement least privilege access
- Use SSH keys instead of passwords
- Encrypt sensitive variables with Ansible Vault
- Regularly rotate credentials

## Integration with Terraform

This Ansible project is designed to work alongside the Terraform infrastructure code in the `../terraform/` directory. The Terraform code provisions the base infrastructure, while Ansible handles the configuration and application deployment.

## Troubleshooting

### Common Issues

1. **SSH Connection Failures**
   - Verify SSH keys are properly configured
   - Check network security groups allow SSH
   - Ensure VMs are running

2. **Azure Authentication Issues**
   - Run `az login` to authenticate
   - Check Azure subscription permissions
   - Verify service principal credentials

3. **Playbook Execution Errors**
   - Use `-v` flag for verbose output
   - Check Ansible logs: `ansible-playbook -i inventory/ playbook.yml -v`
   - Validate variable definitions

### Debugging Commands

```bash
# Test connectivity
ansible -i inventory/ migrated-vms -m ping

# Check facts
ansible -i inventory/ migrated-vms -m setup

# Run specific role
ansible-playbook -i inventory/ playbooks/post-migration.yml --tags azure-vm-config
```

## Contributing

1. Follow Ansible best practices
2. Use descriptive commit messages
3. Test changes in a non-production environment
4. Update documentation for any changes

## License

This project is licensed under the MIT License.
