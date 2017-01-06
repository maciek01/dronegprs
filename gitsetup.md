git init
git remote add origin https://github.com/maciek01/dronegprs.git
git status
git config branch.master.remote origin
git config branch.master.merge refs/heads/master
git config --global user.email "maciek@kolesnik.org"
git config --global user.name "maciek01"
git pull
