from importlib import import_module

from netmiko_bridge.vendor_getter import VendorGetter


class ConnectHandlerDecorator:
    """
    This is a decorator for netmiko ConnectHandler.
    Use this decorator, you can add vendor support by yourself without modify netmiko source code.
    """

    def __init__(self, platforms,
                 vendor_module: str = "netmiko_bridge_vendor", vendor_getter_attr: str = "vendor_getter",
                 *args, **kwargs):
        self.platforms = platforms
        self.vendor_module = vendor_module
        self.vendor_getter_attr = vendor_getter_attr

    def __call__(self, func):
        self.func = func
        return self.wrapper

    def wrapper(self, *args, **kwargs):
        """
        the main wrapper function
        """

        if 'device_type' not in kwargs.keys():
            return self.func(*args, **kwargs)

        device_type = kwargs["device_type"]
        if device_type in self.platforms:
            return self.func(*args, **kwargs)

        vendor_instance = getattr(import_module(self.vendor_module), self.vendor_getter_attr)
        if not isinstance(vendor_instance, VendorGetter):
            # if not isinstance(vendor_instance, VendorGetter.__class__):
            raise AttributeError(
                "The attribute '{}' of module '{}' must be the instance of 'netmiko_bridge.vendor_getter.VendorGetter' "
                .format(self.vendor_getter_attr, self.vendor_module)
            )

        func = vendor_instance.get_class(device_type)

        if func:
            return func(*args, **kwargs)

        return self.func(*args, **kwargs)
