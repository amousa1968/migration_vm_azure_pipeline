resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

module "networking" {
  source = "./modules/networking"

  resource_group_name = azurerm_resource_group.rg.name
  location           = azurerm_resource_group.rg.location
  vnet_name          = var.vnet_name
  vnet_address_space = var.vnet_address_space
  subnet_configs     = var.subnet_configs
  tags               = var.tags

  depends_on = [azurerm_resource_group.rg]
}

module "storage" {
  source = "./modules/storage"

  resource_group_name   = azurerm_resource_group.rg.name
  location             = azurerm_resource_group.rg.location
  storage_account_name = var.storage_account_name
  backup_vault_name    = var.backup_vault_name
  tags                 = var.tags

  depends_on = [azurerm_resource_group.rg]
}