from anet.core import installer
from anet.core.registry import registry

if registry("qtechng-type") == "W":
    # Install toolcat applicatie locally
    execfile("install.py")
