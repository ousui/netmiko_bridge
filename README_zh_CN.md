# Netmiko Bridge

[English](./README.md)|简体中文

这个工程是一个 [Netmiko](https://github.com/ktbyers/netmiko) 的厂商驱动扩展程序。

您可以利用这个模块在 [Netmiko](https://github.com/ktbyers/netmiko) 中添加自己需要的模块，而无需修改 [Netmiko](https://github.com/ktbyers/netmiko) 的源代码。

## 如何构建

首先您需要使用 `pip` 安装 __wheel__ 或 __build__。以下使用 build 举例。

### 使用 __build__

```bash
pip install --upgrade build
```

然后构建模块
```bash
python -m build
```

## 如何安装

### 源码安装

您可以通过文件夹的形式直接安装 __netmiko_bridge__.
```bash
pip install --upgrade {netmiko_bridge_path}
```

### 二进制安装

在构建之后，您可以将本模块安装到您的系统。
```bash
pip install -f {netmiko_bridge_path}/dist/ --upgrade netmiko_bridge
```

### PyPi 安装

抱歉，我还没空上传包到 PyPi.

## 如何使用

### 1. Netmiko 源码修改

要想使用这个模块，需要对 [Netmiko](https://github.com/ktbyers/netmiko) 做一丢丢修改。
在文件 [`netmiko/ssh_dispatcher.py`](https://github.com/ktbyers/netmiko/blob/develop/netmiko/ssh_dispatcher.py) 中 
的 `def ConnectHandler(*args: Any, **kwargs: Any) -> "BaseConnection":` 代码前，添加如下所示代码
```python
import netmiko_bridge
@netmiko_bridge.connect_handler_bridge(platforms, vendor_module = "your_custom_driver_module_package", vendor_getter_attr = "your_custom_vendor_getter_attr_name")
def ConnectHandler(*args: Any, **kwargs: Any) -> "BaseConnection":
    """......"""
```

您也可以给 `ConnectHandler` 的装饰器使用默认值
```python
import netmiko_bridge
@netmiko_bridge.connect_handler_bridge(platforms)
def ConnectHandler(*args: Any, **kwargs: Any) -> "BaseConnection":
    """......"""
```

这是一段快速修改源码的 bash 脚本。这段脚本可以匹配大多数 netmiko 版本。
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

### 2. VendorGetter 实例 

接下来您可以构建您自己的厂商驱动模块，像这样
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

构建更像样的厂商模块，您可以参考模块 [`netmiko_bridge_vendor`](https://github.com/ousui/netmiko_bridge_vendor). 

### 3. Netmiko 使用

现在，您就可以使用自定义的厂商驱动来使用 [Netmiko](https://github.com/ktbyers/netmiko) 了
```python
from netmiko.ssh_dispatcher import ConnectHandler

conn = ConnectHandler(device_type='custom_device')
```
