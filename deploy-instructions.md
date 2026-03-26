# GitHub Setup and Deployment Instructions

## Step 1: Create GitHub Repository

1. In the browser window that just opened, create a new repository:
   - Repository name: `sg-job-ai-impact`
   - Description: "Singapore Job Market AI Impact Visualizer - Analyzing AI exposure across 432 occupations"
   - Visibility: Public
   - **Do NOT** initialize with README, .gitignore, or license (already exists)
   - Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, run these commands in your terminal:

```bash
cd /Users/76321/Documents/VS\ Projects/SG\ JOB\ AI\ Impact

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sg-job-ai-impact.git

# Push the code
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Pages" in the left sidebar
4. Under "Source", select:
   - Branch: `main`
   - Folder: `/site`
5. Click "Save"
6. Wait 1-2 minutes for deployment
7. Your site will be available at: `https://YOUR_USERNAME.github.io/sg-job-ai-impact/`

## Alternative: Quick Deploy Script

Once you've created the repo and added the remote, you can also run:

```bash
cd /Users/76321/Documents/VS\ Projects/SG\ JOB\ AI\ Impact
git push -u origin main

# Then enable GitHub Pages in Settings → Pages
```

## Sharing the Website

Once deployed, share your visualization at:
`https://YOUR_USERNAME.github.io/sg-job-ai-impact/`

The treemap visualization will be fully interactive and can be embedded or shared directly.
