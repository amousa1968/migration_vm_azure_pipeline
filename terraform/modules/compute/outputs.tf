output "vm_scale_set_id" {
  description = "The ID of the VM Scale Set"
  value       = azurerm_linux_virtual_machine_scale_set.vmss.id
}

output "vm_scale_set_name" {
  description = "The name of the VM Scale Set"
  value       = azurerm_linux_virtual_machine_scale_set.vmss.name
}
