import random

class SecurityCamera:
    """Class representing a security camera in the smart home system."""

    def __init__(self, id, status, security_status):
        """Initialize a SecurityCamera instance.

        Args:
            id (str): The unique identifier for the security camera.
            status (bool): The current status of the security camera (True if ON, False if OFF).
            security_status (str): The security status of the camera (SAFE or UNSAFE).
        """
        self.id = id
        self.status = status
        self.security_status = security_status

    def get_id(self):
        """Get the ID of the security camera."""
        return self.id

    def set_id(self, id):
        """Set the ID of the security camera.

        Args:
            id (str): The new ID for the security camera.
        """
        self.id = id
        return self.id

    def get_status(self):
        """Get the status of the security camera (ON or OFF)."""
        return self.status

    def set_status(self, status):
        """Set the status of the security camera.

        Args:
            status (bool): The new status for the security camera (True if ON, False if OFF).
        """
        self.status = status
        return self.status

    def turn_off(self):
        """Turn off the security camera.

        Returns:
            bool: The new status of the security camera (False).
        """
        self.status = False
        return self.status

    def turn_on(self):
        """Turn on the security camera.

        Returns:
            bool: The new status of the security camera (True).
        """
        self.status = True
        return self.status

    def set_security_status(self, security_status):
        """Set the security status of the camera.

        Args:
            security_status (str): The new security status for the camera (SAFE or UNSAFE).
        """
        self.security_status = security_status
        return self.security_status

    def get_security_status(self):
        """Get the security status of the camera."""
        return self.security_status

    def set_random_security_status(self):
        """Set a random security status for the camera."""
        random_status = random.choice(["SAFE", "UNSAFE"])
        self.security_status = random_status
