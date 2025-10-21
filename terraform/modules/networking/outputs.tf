output "vnet_id" {
  description = "The ID of the virtual network"
  value       = azurerm_virtual_network.vnet.id
}

output "vnet_name" {
  description = "The name of the virtual network"
  value       = azurerm_virtual_network.vnet.name
}

output "subnet_ids" {
  description = "Map of subnet names to IDs"
  value       = { for name, subnet in azurerm_subnet.subnets : name => subnet.id }
}

output "nsg_ids" {
  description = "Map of NSG names to IDs"
  value       = { for name, nsg in azurerm_network_security_group.nsg : name => nsg.id }
}