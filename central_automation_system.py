class CentralAutomationSystem:
    """Class representing the central automation system for the smart home."""

    def __init__(self):
        """Initialize a CentralAutomationSystem instance with an empty list of devices."""
        self.devices = []

    def add_device(self, device):
        """Add a device to the automation system.

        Args:
            device: The device to be added to the automation system.
        """
        self.devices.append(device)

    def get_devices(self):
        """Get all devices in the automation system.

        Returns:
            list: A list of devices in the automation system.
        """
        return self.devices

    def remove_device(self, device_id):
        """Remove a device from the automation system by its ID.

        Args:
            device_id (str): The unique identifier of the device to be removed.
        """
        for device in self.devices:
            if device.get_id() == device_id:
                self.devices.remove(device)
                break
