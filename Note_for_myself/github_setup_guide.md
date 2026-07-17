# 🐙 GitHub Setup Guide

A step-by-step reference for pushing your local projects to GitHub.

---

## 🔧 One-Time Setup (Do this only once)

### 1. Install Git
- Download from: https://git-scm.com/downloads
- Use all default options during install
- Verify installation:
  ```bash
  git --version
  ```

### 2. Configure Git with your identity
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 3. Create a GitHub account
- Sign up at: https://github.com

---

## 🚀 For Each New Project

### Step 1 — Create a repo on GitHub (website)
1. Click **+** (top right) → **New repository**
2. Give it a name
3. Click **Create repository**
4. ⚠️ Do **not** check "Initialize this repository" if your files already exist locally

### Step 2 — Go to your project folder in the terminal

**Windows: switch drive first if needed**
```cmd
R:
cd \Your\Project\Folder
```

**Mac/Linux:**
```bash
cd /path/to/your/project
```

### Step 3 — Run these commands (first time only for each project)
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```
> 💡 Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub info.
> The URL is shown on your GitHub repo page after creation.

### ⚠️ If push is rejected (GitHub has files you don't have locally)
This happens when GitHub auto-created a README. Fix it with:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## 📅 Day-to-Day Workflow (After first setup)

Every time you make changes and want to save them to GitHub:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

| Command | What it does |
|---|---|
| `git add .` | 📦 Stages all changed files |
| `git commit -m "..."` | 📸 Saves a snapshot with a label |
| `git push` | ☁️ Uploads snapshot to GitHub |

---

## 🔍 Useful Commands

```bash
git status        # See what files have changed
git log           # See your commit history
git pull          # Download latest changes from GitHub
```

---

## ✅ Good Commit Message Examples

```bash
git commit -m "Add data preprocessing script"
git commit -m "Fix bug in model training loop"
git commit -m "Update README with setup instructions"
```

---

## 💡 Tips

- Run `git status` before `git add .` to see what you're about to stage
- `git push -u origin main` is only needed the **first time** — after that, just `git push`
- On Windows, switch to the correct drive (`R:`, `D:`, etc.) before using `cd`
- Use **Tab** to autocomplete folder names with spaces
