# force_absolute_imports
simple tool that checks only absolute imports are used

```sh
# install
python -m pip install force_absolute_imports

# usage
python -m force_absolute_imports foo.py bar.py python_folder 
```

Pass python files and/or folders. Folders will be recursively scanned for `.py` files

You can pass `--in-place` parameter to fix imports. (it will edit files in place):

```sh
python -m force_absolute_imports --in-place foo.py bar.py python_folder
```
