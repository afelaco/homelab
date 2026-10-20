# -----------------------------
# Login to Azure CLI
# -----------------------------
if [ "$(az account show --query "{user:user.name}" -o tsv)" != "$AZ_USER" ]; then
    echo "  ➡️ Logging in to Azure CLI..."
    az login
    echo "  ✅  Azure CLI login complete!"
else
    echo "  ✅  Already logged in to Azure CLI!"
fi

# -----------------------------
# Create Azure Service Principal for Terraform
# -----------------------------
AZ_SP_TF_NAME="terraform-sp"

if [ -n "$(az ad sp list --display-name "$AZ_SP_TF_NAME" --query '[].appId' -o tsv)" ]; then
    echo "  ✅  Azure Service Principal $AZ_SP_TF_NAME already exists!"
else
    echo "  ➡️ Creating Azure Service Principal $AZ_SP_TF_NAME..."
    export AZ_SP_TF_CREDENTIALS=$(az ad sp create-for-rbac \
        --name "$AZ_SP_TF_NAME" \
        --role Owner \
        --scopes "/subscriptions/$AZ_SUBSCRIPTION_ID" \
        --sdk-auth)
    echo "  ✅  Azure Service Principal $AZ_SP_TF_NAME created!"
fi

# -----------------------------
# Assign Cloud Application Administrator role to Service Principal
# -----------------------------
AZ_SP_TF_OBJECT_ID=$(az ad sp list --display-name "$AZ_SP_TF_NAME" --query "[].id" -o tsv)
AZ_SP_TF_ROLE="Cloud Application Administrator"

echo "  ➡️ Assigning $AZ_SP_TF_ROLE role to Service Principal $AZ_SP_TF_NAME..."
ROLE_TEMPLATE_ID=$(az rest \
    --method GET \
    --url "https://graph.microsoft.com/v1.0/directoryRoles" \
    --query "value[?displayName=='$AZ_SP_TF_ROLE'].id" \
    -o tsv)
az rest \
    --method POST \
    --url "https://graph.microsoft.com/v1.0/directoryRoles/$ROLE_TEMPLATE_ID/members/\$ref" \
    --body "{\"@odata.id\": \"https://graph.microsoft.com/v1.0/directoryObjects/$AZ_SP_TF_OBJECT_ID\"}"
echo "  ✅ Successfully assigned $AZ_SP_TF_ROLE role to Service Principal $AZ_SP_TF_NAME"
