from anet.core.registry import registry
from anet.core import installer

# toolcat installation
installer.initpypackage("anet.imagetools") # removes all files in the package
installer.toolcat(project='imagetools')
