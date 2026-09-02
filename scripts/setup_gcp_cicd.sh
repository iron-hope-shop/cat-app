#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${1:-iron-hope-shop-ff854}"
REGION="${2:-us-central1}"
REPO_NAME="cat-app-repo"
SA_NAME="github-actions-cat-app"

echo "=== 1. Setting project $PROJECT_ID ==="
gcloud config set project "$PROJECT_ID"

echo "=== 2. Enabling GCP APIs ==="
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  iam.googleapis.com \
  cloudbuild.googleapis.com

echo "=== 3. Creating Artifact Registry Repository ==="
if ! gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" &>/dev/null; then
  gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Docker repository for cat-app"
else
  echo "Artifact Registry repository $REPO_NAME already exists."
fi

echo "=== 4. Creating Service Account for GitHub Actions ==="
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="GitHub Actions Deployer for Cat App"
else
  echo "Service Account $SA_NAME already exists."
fi

echo "=== 5. Granting IAM Permissions ==="
# Allow pushing to Artifact Registry
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/artifactregistry.writer" --quiet

# Allow deploying to Cloud Run
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/run.admin" --quiet

# Allow Cloud Run service account impersonation / runtime
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser" --quiet

echo "=== 6. Generating Service Account Key ==="
KEY_FILE="gcp-key.json"
gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account="$SA_EMAIL"

echo ""
echo "=========================================================="
echo "SUCCESS!"
echo "1. Base64/Content of $KEY_FILE needs to be added to GitHub Secrets."
echo "2. Go to: https://github.com/iron-hope-shop/cat-app/settings/secrets/actions"
echo "3. Add a new repository secret:"
echo "   Name:  GCP_SA_KEY"
echo "   Value: (paste contents of $KEY_FILE)"
echo "4. Add secret (optional):"
echo "   Name:  GCP_PROJECT_ID"
echo "   Value: $PROJECT_ID"
echo "5. Remember to delete the local $KEY_FILE once added!"
echo "=========================================================="
