# Compute module (stub)

This is a minimal stub of the compute module used by the migration pipeline.
It provides placeholder resources so CI and `terraform validate` can run without
provisioning actual VMs. Replace these null_resource placeholders with real
`azurerm_*` resources when ready to provision to Azure.

Files:
- `main.tf` - creates placeholder null resources for each VM entry
- `variables.tf` - variable definitions
- `outputs.tf` - outputs for consumption by upstream modules
