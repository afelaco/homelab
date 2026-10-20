TF_BE_CONFIG_FILE="terraform/backend.tf"

if [ ! -f "$TF_BE_CONFIG_FILE" ]; then
    # -----------------------------
    # Create Resource Group
    # -----------------------------
    TF_BE_RG="tfstate-rg"
    TF_BE_RG_LOCATION="northeurope"

    echo "  ➡️ Creating Resource Group: $TF_BE_RG..."
    az group create \
        --name "$TF_BE_RG" \
        --location "$TF_BE_RG_LOCATION"

    # -----------------------------
    # Create Storage Account
    # -----------------------------
    TF_BE_SA="homeautobackend"

    echo "  ➡️ Creating Storage Account: $TF_BE_SA..."
    az storage account create \
        --resource-group "$TF_BE_RG" \
        --name "$TF_BE_SA" \
        --location "$TF_BE_RG_LOCATION" \
        --sku Standard_LRS

    # -----------------------------
    # Get Storage Account key
    # -----------------------------
    echo "  ➡️ Getting Storage Account key..."
    TF_BE_SA_KEY=$(az storage account keys list \
        --resource-group "$TF_BE_RG" \
        --account-name "$TF_BE_SA" \
        --query "[0].value" -o tsv)

    # -----------------------------
    # Create Storage Container
    # -----------------------------
    TF_BE_CONTAINER="tfstate"

    echo "  ➡️ Creating Storage Container: $TF_BE_CONTAINER..."
    az storage container create \
        --account-name "$TF_BE_SA" \
        --account-key "$TF_BE_SA_KEY" \
        --name "$TF_BE_CONTAINER"

    # -----------------------------
    # Write Terraform backend configuration to file
    # -----------------------------
    echo "  ➡️ Writing Terraform backend configuration to $TF_BE_CONFIG_FILE..."
    cat >"$TF_BE_CONFIG_FILE" <<-EOF
terraform {
  backend "azurerm" {
    resource_group_name  = "$TF_BE_RG"
    storage_account_name = "$TF_BE_SA"
    container_name       = "$TF_BE_CONTAINER"
    key                  = "terraform.tfstate"
  }
}
EOF
    echo "  ✅ Terraform backend configuration written to $TF_BE_CONFIG_FILE!"
else
    echo "  ✅ Terraform backend configuration already exists at $TF_BE_CONFIG_FILE!"
fi
