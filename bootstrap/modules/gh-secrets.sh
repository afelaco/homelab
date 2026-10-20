# -----------------------------
# Login to GitHub CLI
# -----------------------------
echo "$GH_TOKEN" | gh auth login --with-token

# -----------------------------
# Set GitHub Actions secrets
# -----------------------------
GH_REPO="afelaco/homeauto"
AZ_KV_SECRETS_FILE="terraform/.terraform.tfvars.json"

echo "  ➡️ Setting secrets in GitHub Actions..."
gh secret set "AZ_SUBSCRIPTION_ID" --repo "$GH_REPO" --body "$AZ_SUBSCRIPTION_ID"
gh secret set "AZ_ADMIN_OBJECT_ID" --repo "$GH_REPO" --body "$AZ_ADMIN_OBJECT_ID"
gh secret set "GH_TOKEN" --repo "$GH_REPO" --body "$GH_TOKEN"
gh secret set "GL_TOKEN" --repo "$GH_REPO" --body "$GL_TOKEN"
gh secret set "AZ_SP_TF_CREDENTIALS" --repo "$GH_REPO" --body "$AZ_SP_TF_CREDENTIALS"
gh secret set "AZ_KV_SECRETS" --repo "$GH_REPO" --body "$(cat "$AZ_KV_SECRETS_FILE")"
echo "  ✅  GitHub Actions secrets set!"
