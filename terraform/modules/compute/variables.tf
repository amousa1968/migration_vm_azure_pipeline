variable "vm_scale_set_name" {
  description = "Name of the VM Scale Set for high availability"
  type        = string
}

variable "location" {
  description = "Azure region for the VM Scale Set"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "vm_size" {
  description = "Size of the VMs in the scale set"
  type        = string
}

variable "admin_username" {
  description = "Admin username for the VMs"
  type        = string
}

variable "admin_password" {
  description = "Admin password for the VMs"
  type        = string
  sensitive   = true
}

variable "subnet_id" {
  description = "ID of the subnet for the VM Scale Set"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the VM Scale Set"
  type        = map(string)
  default     = {}
}
