class VendorGetter:
    """
    vendor device connection class getter
    """

    def __init__(self):
        self._mapper = {}

    def add_vendor(self, vendor: dict):
        self._mapper.update(vendor)

    def get_class(self, device_type: str):
        return self._mapper.get(device_type)

    def supports(self) -> dict:
        return self._mapper
