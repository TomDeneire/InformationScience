jupyter-book build course/
git add .
git commit -m "Build"
ghp-import -n -p -f course/_build/html
