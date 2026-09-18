# Push this final EYENEX code to the existing GitHub repository

Repository:
`https://github.com/Hamzabinmaqsood/https-Eyenex-Training-Consultancy-Services`

The safest method is to **clone the existing repository first**, then replace its tracked working files with this final package. This preserves the existing Git history.

## 1. Install Git for Windows

Verify in PowerShell:

```powershell
git --version
```

## 2. Clone the existing repository

```powershell
cd $HOME\Desktop
git clone https://github.com/Hamzabinmaqsood/https-Eyenex-Training-Consultancy-Services.git EyenexGitHub
git -C EyenexGitHub checkout main
git -C EyenexGitHub pull origin main
```

## 3. Replace the repository files with this final package

Extract `EYENEX_Final_GitHub_Ready.zip` somewhere, for example:

`C:\Users\Malik\Desktop\EYENEX_Final_GitHub_Ready`

Then run:

```powershell
cd $HOME\Desktop\EyenexGitHub
git rm -r .
robocopy "$HOME\Desktop\EYENEX_Final_GitHub_Ready" "." /E /XD .git venv .venv __pycache__
```

`robocopy` may return a non-zero code even when copying succeeded; review the summary and continue if files were copied normally.

## 4. Review what will be committed

```powershell
git status
git diff --stat
git diff -- .gitignore core/context_processors.py admissions/views.py config/settings.py
```

Confirm that files such as `db.sqlite3`, `.env`, private payment screenshots, and `private_media` are **not** staged.

## 5. Commit

```powershell
git add -A
git status
git commit -m "Finalize EYENEX production website and deployment updates"
```

## 6. Push to GitHub

```powershell
git push origin main
```

If GitHub asks you to authenticate over HTTPS, use the browser/Git Credential Manager flow or a Personal Access Token. Do not use your GitHub account password as the Git password.

## 7. Verify online

Open the repository and confirm the latest commit is visible on `main`.

Check that the repository does **not** expose:

- `db.sqlite3`
- `.env`
- production secret keys
- student/application data
- payment screenshots

## Optional: future updates

For later code changes, work inside the cloned `EyenexGitHub` folder and use:

```powershell
git pull origin main
git status
git add -A
git commit -m "Describe the update"
git push origin main
```
