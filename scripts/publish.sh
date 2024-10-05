
#!/usr/bin/env bash

# Exit the script if any command fails
set -e

# Check if a tag argument is provided
if [ -z "$1" ]; then
  echo "Error: Tag name is required"
  echo "Usage: $0 <tag-name>"
  exit 1
fi

TAG_NAME=$1

# Switch to the main branch and pull the latest changes
echo "Switching to the 'main' branch and pulling the latest changes..."
git checkout main
git pull origin main

# Create a new tag
echo "Creating a new tag: $TAG_NAME"
git tag "$TAG_NAME"

# Push the tag to the remote repository
echo "Pushing the new tag to the remote repository..."
git push origin "$TAG_NAME"
git push origin --tags

# Switch back to the development branch
echo "Switching back to the 'dev' branch..."
git checkout dev

echo "Tagging and push completed successfully!"
