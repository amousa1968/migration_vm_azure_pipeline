# Azure VM Migration Pipeline

This project implements an automated pipeline for migrating virtual machines (VMs) from on-premises VMware environments to Azure Cloud, following a 5-phase process using Azure Migrate, Terraform, and Ansible.

## Overview

The pipeline automates the migration of VMware VMs to Azure with minimal manual intervention, enabling Day 2 operations like backups, monitoring, security, and compliance.

## Tools Used

- Azure Migrate: Discovery, replication, and migration of VMs
- Terraform: Infrastructure provisioning and lifecycle management
- Ansible: Migration orchestration, post-migration configuration, and Day 2 operations
- GitHub: Source control, CI/CD orchestration, and collaboration

## Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed and configured (`az login` to authenticate)
- Terraform (≥ 1.0) installed
- Ansible (≥ 3.9) installed with Azure collection (`ansible-galaxy collection install azure.azcollection`)
- SSH key pair for VM access
- On-premises VMware environment accessible by Azure Migrate

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd azure_migration_vmware
```

2. Configure Azure Credentials
- Set up Azure service principal and store credentials in GitHub Secrets (for CI/CD) or environment variables
- Update `ansible/inventory.ini` with VM IPs and Azure credentials

3. Configure Terraform Variables
- Edit `terraform/terraform.tfvars` to set your desired values for resource names, locations, etc.

4. Initialize Terraform
```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

5. Resources Created

The Terraform configuration is valid and includes 18 Azure resources that would be created, including:

- Resource Group
- Virtual Network and Subnets (dynamic)
- Network Security Group with RDP/SSH rules
- Storage Account
- Recovery Services Vault
- Backup Policy
- Linux Virtual Machine Scale Set (2 instances, Ubuntu 18.04-LTS)

The plan use Azure to authentication, and apply the configuration create all necessary infrastructure for VM migration with high availability via VM Scale Set.

6. Configure Ansible
- Update `ansible/inventory.ini` with on-premises and Azure VM details
- Ensure SSH keys are set up for passwordless access

## Usage

### Manual Execution

Run individual phases using Ansible playbooks:

```bash
# Phase 2: VM Migration
ansible-playbook ansible/playbooks/migrate_vm.yml

# Phase 3: Post-Migration Setup
ansible-playbook ansible/playbooks/post_migration.yml
```

### CI/CD Execution

The GitHub workflow orchestrates all phases sequentially. Trigger via:
- Push to main branch
- Manual workflow dispatch with VM name and environment inputs

## Project Structure

```
azure_migration_vmware/
├── terraform/                    # Infrastructure as Code
│   ├── main.tf                  # Main Terraform configuration
│   ├── variables.tf             # Variable definitions
│   ├── outputs.tf               # Output definitions
│   ├── provider.tf              # Provider configuration
│   ├── terraform.tfvars         # Variable values
│   └── modules/                 # Reusable modules
├── ansible/                     # Automation scripts
│   ├── ansible.cfg             # Ansible configuration
│   ├── inventory.ini           # Inventory file
│   └── playbooks/              # Ansible playbooks
├── .github/workflows/          # CI/CD pipelines
│   └── migration-pipeline.yml  # GitHub Actions workflow
└── README.md                   # Project documentation
```

## Limitations

- OS Support: Does not support legacy OS (Windows Server 2016 or older, RHEL 7 or older)
- Database Migration: Azure Migrate does not support transactional replication for databases
- User Access Management: Automated user access for Linux VMs is not supported

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request
