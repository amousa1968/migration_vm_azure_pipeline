output "storage_account_id" {
  description = "The ID of the storage account"
  value       = azurerm_storage_account.storage.id
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.storage.name
}

output "backup_vault_id" {
  description = "The ID of the backup vault"
  value       = azurerm_recovery_services_vault.vault.id
}

output "backup_policy_id" {
  description = "The ID of the VM backup policy"
  value       = azurerm_backup_policy_vm.backup_policy.id
}