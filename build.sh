jupyter-book build course/
ghp-import -n -p -f course/_build/html
git add .
git commit -m "jupyter-book"
git push
