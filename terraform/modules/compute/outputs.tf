output "vm_names" {
  value = [for r in null_resource.vm_placeholder : r.triggers.name]
}
