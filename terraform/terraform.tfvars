resource_group_name = "vm-migration-rg"
location            = "eastus2"
environment         = "prod"
vnet_name           = "migration-vnet"
vnet_address_space  = ["10.0.0.0/16"]

subnet_configs = [
  {
    name              = "migration-subnet"
    address_prefixes  = ["10.0.1.0/24"]
    service_endpoints = ["Microsoft.Storage"]
  },
  {
    name              = "management-subnet"
    address_prefixes  = ["10.0.2.0/24"]
    service_endpoints = ["Microsoft.Storage"]
  }
]

storage_account_name = "vmmigrationstorageacct"
backup_vault_name    = "vm-backup-vault"

tags = {
  Environment = "Production"
  Project     = "VM-Migration"
  ManagedBy   = "Terraform"
}