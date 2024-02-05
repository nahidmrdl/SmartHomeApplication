import time
from datetime import datetime

class SmartLight:
    """Class representing a smart light in the smart home system."""

    def __init__(self, id, status, brightness):
        """Initialize a SmartLight instance.

        Args:
            id (str): The unique identifier for the smart light.
            status (bool): The current status of the smart light (True if ON, False if OFF).
            brightness (int): The brightness level of the smart light (0 to 100).
        """
        self.id = id
        self.status = status
        self.brightness = brightness

    def set_brightness(self, brightness):
        """Set the brightness level of the smart light.

        Args:
            brightness (int): The new brightness level (0 to 100).

        Returns:
            int: The new brightness level of the smart light.
        """
        self.brightness = brightness
        return self.brightness

    def get_brightness(self):
        """Get the current brightness level of the smart light."""
        return self.brightness

    def get_status(self):
        """Get the status of the smart light (ON or OFF)."""
        return self.status

    def set_status(self, status):
        """Set the status of the smart light.

        Args:
            status (bool): The new status for the smart light (True if ON, False if OFF).

        Returns:
            bool: The new status of the smart light.
        """
        self.status = status
        return self.status

    def get_id(self):
        """Get the ID of the smart light."""
        return self.id

    def set_id(self, id):
        """Set the ID of the smart light.

        Args:
            id (str): The new ID for the smart light.

        Returns:
            str: The new ID of the smart light.
        """
        self.id = id
        return self.id

    def turn_off(self):
        """Turn off the smart light.

        Returns:
            bool: The new status of the smart light (False).
        """
        if self.status:
            for _ in range(100):
                self.brightness -= 1
                time.sleep(0.1)
                if self.brightness == 0:
                    break
            self.status = False
        return self.status

    def turn_on(self):
        """Turn on the smart light.

        Returns:
            bool: The new status of the smart light (True).
        """
        if not self.status:
            for _ in range(100):
                self.brightness += 1
                time.sleep(0.1)
                if self.brightness == 100:
                    break
            self.status = True
        return self.status
