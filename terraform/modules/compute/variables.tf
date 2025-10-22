variable "vm_list" {
  description = "List of VM definitions to manage (stub)"
  type = list(object({
    name = string
  }))
  default = []
}
