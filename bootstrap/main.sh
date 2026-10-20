#!/usr/bin/env bash
set -euo pipefail

# -----------------------------
# Set current working directory
# -----------------------------
cd "$(git rev-parse --show-toplevel)"

# -----------------------------
# Load configuration
# -----------------------------
source bootstrap/.env

# -----------------------------
# Sync system environment with Brewfile
# -----------------------------
echo "➡️ Syncing system environment with Brewfile..."
brew bundle check || brew bundle
echo "✅ System environment synced!"

# -----------------------------
# Set repo level Git identity
# -----------------------------
echo "➡️ Setting Git identity on repo level..."
source bootstrap/modules/git-config.sh
echo "✅ Git bootstrap complete!"

# -----------------------------
# Set GitHub Actions secrets
# -----------------------------
#echo "➡️ Setting GitHub Actions secrets..."
#source bootstrap/modules/gh-secrets.sh
#echo "✅ GitHub bootstrap complete!"

# -----------------------------
# Sync virtual environment
# -----------------------------
#echo "➡️ Syncing virtual environment..."
#uv sync --all-groups
#echo "✅ Virtual environment synced!"

# -----------------------------
# Install pre-commit hooks
# -----------------------------
#echo "➡️ Installing pre-commit hooks..."
#uv run pre-commit clean
#uv run pre-commit install
#echo "✅ Pre-commit hooks installed!"

# -----------------------------
# Bootstrap complete
# -----------------------------
echo "✅ Bootstrap complete!"
