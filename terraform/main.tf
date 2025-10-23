resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

module "networking" {
  source = "./modules/networking"

  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  vnet_name           = var.vnet_name
  vnet_address_space  = var.vnet_address_space
  subnet_configs      = var.subnet_configs
  tags                = var.tags

  depends_on = [azurerm_resource_group.rg]
}

module "storage" {
  source = "./modules/storage"

  resource_group_name  = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  storage_account_name = var.storage_account_name
  backup_vault_name    = var.backup_vault_name
  tags                 = var.tags

  depends_on = [azurerm_resource_group.rg]
}

module "compute" {
  source = "./modules/compute"

  vm_scale_set_name  = var.vm_scale_set_name
  location           = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  vm_size            = var.vm_size
  admin_username     = var.admin_username
  admin_password     = var.admin_password
  subnet_id          = module.networking.subnet_ids["migration"]
  tags               = var.tags

  depends_on = [module.networking]
}
