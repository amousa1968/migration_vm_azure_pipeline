terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  # Using local state for testing/mock purposes
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "azurerm" {
  # Use mock credentials for testing
  features {
    virtual_machine {
      delete_os_disk_on_deletion     = true
      skip_shutdown_and_force_delete = false
    }
  }
  
  # Mock subscription for testing
  subscription_id = "00000000-0000-0000-0000-000000000000"
  client_id       = "00000000-0000-0000-0000-000000000000"
  client_secret   = "mock-client-secret"
  tenant_id       = "00000000-0000-0000-0000-000000000000"
  
  # Skip provider authentication for testing
  skip_provider_registration = true
}