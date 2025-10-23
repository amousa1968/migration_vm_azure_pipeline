# Compute module

This module provisions an Azure Virtual Machine Scale Set (VMSS) for high availability post-migration. The VMSS provides automatic scaling, load balancing, and fault tolerance for migrated VMs.

## Resources Created

- `azurerm_linux_virtual_machine_scale_set` - VM Scale Set with Linux VMs

## Features

- High availability through VM Scale Set
- Automatic scaling capabilities
- Integrated load balancing
- Support for Ubuntu 22.04 LTS
- Configurable VM sizes and instance counts
- Network integration with existing subnets

## Usage

```hcl
module "compute" {
  source = "./modules/compute"

  vm_scale_set_name  = "migration-vmss-prod"
  location           = "East US"
  resource_group_name = "migration-rg"
  vm_size            = "Standard_DS1_v2"
  admin_username     = "azureuser"
  admin_password     = "P@ssw0rd123!"
  subnet_id          = module.networking.subnet_ids["migration"]
  tags               = var.tags
}
```

## Inputs

- `vm_scale_set_name` - Name of the VM Scale Set
- `location` - Azure region
- `resource_group_name` - Resource group name
- `vm_size` - VM size (e.g., Standard_DS1_v2)
- `admin_username` - Admin username
- `admin_password` - Admin password
- `subnet_id` - Subnet ID for network interface
- `tags` - Resource tags

## Outputs

- `vm_scale_set_id` - VM Scale Set resource ID
- `vm_scale_set_name` - VM Scale Set name
