locals {
  vm_names = [for vm in var.vm_list : vm.name]
}

resource "null_resource" "vm_placeholder" {
  for_each = toset(local.vm_names)

  triggers = {
    name = each.key
  }
}
