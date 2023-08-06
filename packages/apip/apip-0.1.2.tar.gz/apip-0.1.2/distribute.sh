rm -rf apip.egg-info
rm -rf dist
py -m build
twine upload dist/*