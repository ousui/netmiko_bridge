# Netmiko Bridge

This is a decorator for Netmiko vendor driver extension.

You can use this mod to add yourself vendor driver without modify netmiko source code.

## How to build

First you must install __wheel__ or __build__ with pip.

### use build

```bash
pip install --upgrade build
```

Then you can build this module.
```bash
python -m build
```

## How to install

### Install without build

You can install __netmiko_bridge__ direct with directory.
```bash
pip install --upgrade {netmiko_bridge_path}
```

### Install with binary package

The last you can install the module to your system.
```bash
pip install netmiko_bridge
```

## How to use

### 1. Netmiko source code modify
To use this module, you must do some minimal modify in netmiko.

With the file in `netmiko/ssh_dispatcher.py`, please add this code before `def ConnectHandler(*args: Any, **kwargs: Any) -> "BaseConnection":`, like this
```python
import netmiko_bridge
@netmiko_bridge.connect_handler_bridge(platforms, vendor_module = "your_custom_driver_module_package", vendor_getter_attr = "your_custom_vendor_getter_attr_name")
def ConnectHandler(*args: Any, **kwargs: Any) -> "BaseConnection":
    """......"""
```

You can also use the default value on the `ConnectHandler` decorator
```python
import netmiko_bridge
@netmiko_bridge.connect_handler_bridge(platforms)
def ConnectHandler(*args: Any, **kwargs: Any) -> "BaseConnection":
    """......"""
```

This the bash script help you to modify the source code, and it can match more netmiko version.
```bash
_python_lib_path=/usr/lib64/python3.6/site-packages
_netmiko_fix_file=${_python_lib_path}/netmiko/ssh_dispatcher.py
if [ -f "${_netmiko_fix_file}" ]; then
  _netmiko_fixed=$(grep -c "@netmiko_bridge.connect_handler_bridge" ${_netmiko_fix_file})
  if [ "${_netmiko_fixed}" -eq "0" ]; then
    sed -i "s/def ConnectHandler/import netmiko_bridge\n@netmiko_bridge.connect_handler_bridge(platforms)\ndef ConnectHandler/" ${_netmiko_fix_file}
  fi
fi
```

### 2. VendorGetter Instance 

Then you can build yourself vendor driver module like this
```python
from netmiko_bridge.vendor_getter import VendorGetter
from netmiko.cisco_base_connection import CiscoBaseConnection


class Custom(CiscoBaseConnection):
    """Your Custom Vendor Support"""

    def __init__(self):
        pass


vendor_getter = VendorGetter()
# you can add the mapper use the
vendor_getter.add_vendor({
    "custom_device": Custom
})
```
