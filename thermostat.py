class Thermostat:
    """Class representing a thermostat in the smart home system."""

    def __init__(self, id, status, temperature):
        """Initialize a Thermostat instance.

        Args:
            id (str): The unique identifier for the thermostat.
            status (bool): The current status of the thermostat (True if ON, False if OFF).
            temperature (float): The current temperature set on the thermostat.
        """
        self.id = id
        self.status = status
        self.temperature = temperature

    def get_id(self):
        """Get the ID of the thermostat."""
        return self.id

    def set_id(self, id):
        """Set the ID of the thermostat.

        Args:
            id (str): The new ID for the thermostat.
        """
        self.id = id
        return self.id

    def get_status(self):
        """Get the status of the thermostat (ON or OFF)."""
        return self.status

    def set_status(self, status):
        """Set the status of the thermostat.

        Args:
            status (bool): The new status for the thermostat (True if ON, False if OFF).
        """
        self.status = status
        return self.status

    def turn_off(self):
        """Turn off the thermostat.

        Returns:
            bool: The new status of the thermostat (False).
        """
        self.status = False
        return self.status

    def turn_on(self):
        """Turn on the thermostat.

        Returns:
            bool: The new status of the thermostat (True).
        """
        self.status = True
        return self.status

    def set_temperature(self, temperature):
        """Set the temperature on the thermostat.

        Args:
            temperature (float): The new temperature set on the thermostat.
        """
        self.temperature = temperature
        return self.temperature

    def get_temperature(self):
        """Get the current temperature set on the thermostat."""
        return self.temperature
