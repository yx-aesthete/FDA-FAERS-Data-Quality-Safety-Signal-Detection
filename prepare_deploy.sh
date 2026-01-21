#!/bin/bash

echo "🚀 Preparing FAERS PoC for Deployment"
echo ""

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo ""
echo "📝 Staging files for commit..."
git add .

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short

# Create initial commit
echo ""
read -p "Create commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "FDA FAERS PoC Dashboard - Ready for deployment"
    echo "✅ Commit created"
fi

echo ""
echo "✨ Repository prepared for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Create GitHub repository at https://github.com/new"
echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
echo "5. Deploy on Railway: https://railway.app"
echo ""
echo "🎯 Or use Streamlit Cloud: https://share.streamlit.io"
