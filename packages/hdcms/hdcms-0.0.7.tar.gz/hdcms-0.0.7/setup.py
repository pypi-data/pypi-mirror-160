from setuptools import setup, Extension
import numpy as np
import sysconfig
import toml

p = toml.load("pyproject.toml")["project"]
name = p["name"]
package_info = {
    "name": name,  # used in `pip install <name>`
    "version": p["version"],
    "description": p["description"],
    "author": p["authors"][0]["name"],
    "author_email": p["authors"][0]["email"],
}

include = [np.get_include(), sysconfig.get_path("include")]
source = ["python.c"]
# used in `import <name>`
module = Extension(name, source, include_dirs=include)

setup(**package_info, ext_modules=[module])
