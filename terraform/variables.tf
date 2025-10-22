variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region for resources"
  type        = string
}

variable "environment" {
  description = "Environment name (e.g., prod, dev, staging)"
  type        = string
}

variable "vnet_name" {
  description = "Name of the virtual network"
  type        = string
}

variable "vnet_address_space" {
  description = "Address space for the virtual network"
  type        = list(string)
}

variable "subnet_configs" {
  description = "Configuration for subnets"
  type = list(object({
    name              = string
    address_prefixes  = list(string)
    service_endpoints = optional(list(string))
  }))
}

variable "storage_account_name" {
  description = "Name of the storage account"
  type        = string
}

variable "backup_vault_name" {
  description = "Name of the backup vault"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
}