# pathimport #

This simple python module allows to elegantly handle project imports on python without headaches.

### Why pathimport? ###
Using import statements inside python projects can lead to numerous headaches and subtle problems. Importing in python requires a deep understanding of how the interpreter loads other modules and scripts on runtime. A misuse of imports can lead to problems when your project is deployed outside your development environment; and even before that, imports can hide many pitfalls. This package wants to simplify the life of python users, allowing them to perform imports from other scripts of the same project effortlessly.
   
   
### Installation ###
The pathimport module can be installed through pip.
```
pip install pathimport
```

### Usage ###
Let's suppose to have a python project with the following structure.

    module
	├── submodule_a                            
	│   └── script_a.py                    
	├── submodule_b
	│   └── script_b.py
	└── common.py

Inside `common.py` we have defined the following function,
```python
def fun_common():
    # do things...
```

while in `script_a.py` we have defined the following.
```python
def fun_a():
    # do things...
```

To avoid the usage of relative imports, pathimport can be used to load these functions inside `script_b.py`.

```python
from pathimport import set_module_root
set_module_root("..")

# from now on all the imports can be
# perfomed from the module root
from common import fun_common
from submodule_a import fun_a

if __name__ == "__main__":
    fun_common()
    fun_a()
```

Optionally, the module/project name can be used as a prefix.

```python
from pathimport import set_module_root
set_module_root("..", prefix=True)

from module.common import fun_common
from module.submodule_a import fun_a
```

# Under The Hood #
To resolve the interpreter import ambiguities, the `set_module_root` of pathimport modifies the `PATH` environment variable to point to the module root (or to the preceding directory if *prefix* is set to *True*). For this reason, the interpreter will be able to correctly localize and import your scripts from the filesystem, without additional problems that can arise depending on the current working directory, or if the source code is launched as a script or as a module.

### Additional Resources ###
* [Stack Overflow question on relative imports](https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time)
