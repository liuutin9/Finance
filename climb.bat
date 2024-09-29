@echo off
chcp 65001
cd "C:\Users\Utin Liu\OneDrive\桌面\Finance\"
git pull --rebase
py climb.py
py stock_repo.py
git checkout main
git add .
git commit -m "daily update"
git push -u origin main
pause
exit