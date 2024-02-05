from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QSlider, QTextEdit, QVBoxLayout, \
    QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QTimer
from smart_home.smart_light import SmartLight
from smart_home.thermostat import Thermostat
from smart_home.security_camera import SecurityCamera


class SmartHomeGUI(QMainWindow):
    """Class representing the Smart Home Monitoring Dashboard."""
    def __init__(self, automation_system):
        """Initialize a SmartHomeGUI instance.

                Args:
                    automation_system: The central automation system for the smart home.
                """
        super().__init__()
        self.automation_system = automation_system
        self.smart_light = None
        self.thermostat = None
        self.security_camera = None

        self.setWindowTitle("Smart Home Dashboard")

        self.setWindowIcon(QIcon('icon.png'))


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)


        self.create_widgets()
        self.update_device_status()

        self.toggle_timer = QTimer()
        self.toggle_timer.timeout.connect(self.update_brightness_slider)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#ccccff"))
        self.setPalette(p)




    def create_widgets(self):
        """Create the widgets for the Smart Home Monitoring Dashboard."""

        layout = QVBoxLayout()

        self.add_device_label = QLabel("Add New Device:")
        layout.addWidget(self.add_device_label)

        self.device_type_label = QLabel("Device Type:")
        layout.addWidget(self.device_type_label)

        self.device_type_dropdown = QComboBox()
        self.device_type_dropdown.addItems(["Smart Light", "Thermostat", "Security Camera"])
        layout.addWidget(self.device_type_dropdown)

        self.device_id_label = QLabel("Device ID:")
        layout.addWidget(self.device_id_label)

        self.device_id_textfield = QLineEdit()
        layout.addWidget(self.device_id_textfield)

        self.add_device_button = QPushButton("Add Device")
        self.add_device_button.clicked.connect(self.add_new_device)
        layout.addWidget(self.add_device_button)

        self.remove_device_label = QLabel("Remove Device:")
        layout.addWidget(self.remove_device_label)

        self.remove_device_dropdown = QComboBox()
        self.remove_device_dropdown.addItem("Select Device to Remove")
        layout.addWidget(self.remove_device_dropdown)

        self.remove_device_button = QPushButton("Remove Device")
        self.remove_device_button.clicked.connect(self.remove_selected_device)
        layout.addWidget(self.remove_device_button)

        self.light_status_label = QLabel("Light Status:")
        layout.addWidget(self.light_status_label)

        self.light_button_toggle = QPushButton("Toggle Light")
        self.light_button_toggle.clicked.connect(self.toggle_smart_light)
        layout.addWidget(self.light_button_toggle)

        self.light_button_toggle.setStyleSheet(
            """
            QPushButton {
                background-color: green;
                color: white;
                border: 2px solid grey;
                border-radius: 5px;
                min-height: 30px;
            }

            QPushButton:hover {
                background-color: darkgreen;  
                color: yellow;               
                border-color: darkgrey;       
            }
            """
        )

        layout.addWidget(self.light_button_toggle)

        self.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                border: 2px solid #2980b9;
                border-radius: 5px;
                min-height: 30px;
            }

            QPushButton:hover {
                background-color: #2980b9;
                color: #ffffff;
                border-color: #3498db;
            }
            """
        )

        self.light_brightness_label = QLabel("Brightness:")
        layout.addWidget(self.light_brightness_label)

        self.light_brightness_slider = QSlider(orientation=1)
        self.light_brightness_slider.setRange(0, 100)
        self.light_brightness_slider.valueChanged.connect(self.update_device_status)
        layout.addWidget(self.light_brightness_slider)

        self.thermostat_status_label = QLabel("Thermostat Status:")
        layout.addWidget(self.thermostat_status_label)

        self.thermostat_button_toggle = QPushButton("Toggle Thermostat")
        self.thermostat_button_toggle.clicked.connect(self.toggle_thermostat)
        layout.addWidget(self.thermostat_button_toggle)

        self.thermostat_button_toggle.setStyleSheet(
            """
            QPushButton {
                
                background-color: red;
                color: white;
                border: 2px solid grey;
                border-radius: 5px;
                min-height: 30px;
            }

            QPushButton:hover {
                background-color: darkred; 
                color: yellow;            
                border-color: darkgrey;  
            }
            """
        )

        layout.addWidget(self.thermostat_button_toggle)

        self.thermostat_slider = QSlider(orientation=1)
        self.thermostat_slider.setRange(0, 100)
        self.thermostat_slider.valueChanged.connect(self.update_device_status)
        layout.addWidget(self.thermostat_slider)

        self.security_status_label = QLabel("Security Camera Status:")
        layout.addWidget(self.security_status_label)

        self.security_button_toggle = QPushButton("Toggle Camera")
        self.security_button_toggle.clicked.connect(self.toggle_security_camera)
        layout.addWidget(self.security_button_toggle)

        self.security_button_toggle.setStyleSheet(
            """
            QPushButton {
                background-color: black;
                color: white;
                border: 2px solid grey;
                border-radius: 5px;
                min-height: 30px;
            }

            QPushButton:hover {
                background-color: #2f3030; 
                color: white;                
                border-color: black;      
            }
            """
        )
        layout.addWidget(self.security_button_toggle)

        self.show_security_status_button = QPushButton("Show Security Status")
        self.show_security_status_button.clicked.connect(self.show_security_status)
        layout.addWidget(self.show_security_status_button)

        # Monitoring Section
        self.monitoring_label = QLabel("Monitoring:")
        layout.addWidget(self.monitoring_label)

        self.monitoring_text = QTextEdit()
        layout.addWidget(self.monitoring_text)


        layout.setContentsMargins(20, 20, 20, 20)

        self.central_widget.setLayout(layout)

    def add_new_device(self):
        """Add a new device to the smart home system based on user input."""
        device_type = self.device_type_dropdown.currentText()
        device_id = self.device_id_textfield.text()

        if not device_id:
            self.show_message("Error", "Device ID is not provided.")
            return

        # Check if the device ID already exists for the given device type
        existing_ids = [device.get_id() for device in self.automation_system.get_devices() if
                        isinstance(device, SmartLight) and device_type == "Smart Light"
                        or isinstance(device, Thermostat) and device_type == "Thermostat"
                        or isinstance(device, SecurityCamera) and device_type == "Security Camera"]
        if device_id in existing_ids:
            self.show_message("Error", f"Device with ID '{device_id}' already exists for the selected device type.")
            return

        if device_type == "Smart Light":
            self.smart_light = SmartLight(id=device_id, status=False, brightness=0.0)
            try:
                self.automation_system.add_device(self.smart_light)
                self.update_remove_device_dropdown()
                self.show_message("Successful Operation", "Smart Light added successfully.")
            except Exception as e:
                self.show_message("Error", f"Error adding Smart Light: {str(e)}")
            self.update_device_status()
        elif device_type == "Thermostat":
            self.thermostat = Thermostat(id=device_id, status=False, temperature=0.0)
            try:
                self.automation_system.add_device(self.thermostat)
                self.update_remove_device_dropdown()
                self.show_message("Success", "Thermostat added successfully.")
            except Exception as e:
                self.show_message("Error", f"Error adding Thermostat: {str(e)}")
            self.update_device_status()
        elif device_type == "Security Camera":
            self.security_camera = SecurityCamera(id=device_id, status=False,
                                                  security_status="Click 'Show Security Status' to get the status")
            try:
                self.automation_system.add_device(self.security_camera)
                self.update_remove_device_dropdown()
                self.show_message("Success", "Security Camera added successfully.")
            except Exception as e:
                self.show_message("Error", f"Error adding Security Camera: {str(e)}")
            self.update_device_status()

    def show_message(self, title, message):
        """Show a message box with the given title and message."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def update_remove_device_dropdown(self):
        """Update the remove device dropdown with the list of devices in the smart home system."""
        self.remove_device_dropdown.clear()
        self.remove_device_dropdown.addItem("Select Device to Remove")

        for device in self.automation_system.get_devices():
            if isinstance(device, SmartLight):
                item_text = f"SmartLight#{device.get_id()}"
            elif isinstance(device, SecurityCamera):
                item_text = f"SecurityCamera#{device.get_id()}"
            elif isinstance(device, Thermostat):
                item_text = f"Thermostat#{device.get_id()}"
            else:
                item_text = device.get_id()
            self.remove_device_dropdown.addItem(item_text, userData=device.get_id())

    def remove_selected_device(self):
        """Remove the selected device from the smart home system."""
        selected_device_index = self.remove_device_dropdown.currentIndex()
        if selected_device_index != 0:
            device_id = self.remove_device_dropdown.itemData(selected_device_index)
            if device_id:

                if self.smart_light and self.smart_light.get_id() == device_id:
                    self.smart_light = None
                    self.light_brightness_slider.setValue(0)

                    self.toggle_timer.stop()
                elif self.thermostat and self.thermostat.get_id() == device_id:
                    self.thermostat = None
                    self.thermostat_slider.setValue(0)
                elif self.security_camera and self.security_camera.get_id() == device_id:
                    self.security_camera = None

                self.automation_system.remove_device(device_id)
                self.update_remove_device_dropdown()
                self.update_device_status()

    def toggle_smart_light(self):
        """Toggle the status of the smart light and update the device status."""
        if self.smart_light:
            if self.smart_light.status:
                self.smart_light.turn_off()
                self.toggle_timer.start(100)
            else:
                self.smart_light.turn_on()
                self.toggle_timer.start(100)

    def toggle_thermostat(self):
        """Toggle the status of the thermostat and update the device status."""
        if self.thermostat:
            if self.thermostat.status:
                self.thermostat.turn_off()
            else:
                self.thermostat.turn_on()
        self.update_device_status()

    def toggle_security_camera(self):
        """Toggle the status of the security camera and update the device status."""
        if self.security_camera:
            if self.security_camera.status:
                self.security_camera.turn_off()
            else:
                self.security_camera.turn_on()
        self.update_device_status()

    def update_brightness_slider(self):
        """Update the brightness slider based on the status of the smart light."""
        current_value = self.light_brightness_slider.value()
        if self.smart_light.status:
            if current_value < 100:
                new_value = current_value + 1
                self.light_brightness_slider.setValue(new_value)
            else:
                self.toggle_timer.stop()
        else:
            if current_value > 0:
                new_value = current_value - 1
                self.light_brightness_slider.setValue(new_value)
            else:
                self.toggle_timer.stop()
        self.update_device_status()

    def update_device_status(self):
        """Update the status of devices on the monitoring dashboard."""
        if self.smart_light:
            light_status = "ON" if self.smart_light.status else "OFF"
            light_brightness = self.light_brightness_slider.value()
        else:
            light_status = "N/A"
            light_brightness = 0

        if self.thermostat:
            thermostat_status = "ON" if self.thermostat.status else "OFF"
            thermostat_temperature = self.thermostat_slider.value()
        else:
            thermostat_status = "N/A"
            thermostat_temperature = 0

        if self.security_camera:
            security_camera_status = "ON" if self.security_camera.status else "OFF"
            security_status = self.security_camera.security_status if self.security_camera.status else "Unable to get the security status, the camera is OFF"
        else:
            security_camera_status = "N/A"
            security_status = "N/A"

        self.show_security_status_button.setEnabled(self.security_camera.status if self.security_camera else False)
        self.thermostat_slider.setEnabled(self.thermostat.status if self.thermostat else False)
        self.light_brightness_slider.setEnabled(self.smart_light.status if self.smart_light else False)

        if self.smart_light and self.smart_light.status:
            # Slider is enabled
            self.light_brightness_slider.setEnabled(True)
            self.light_brightness_slider.setStyleSheet(
                """
               QSlider {
                   height: 20px; 
               }
               QSlider::groove:horizontal {
                   background-color: #e0e0e0; 
                   border: 1px solid #cccccc; 
                   height: 4px;
                   margin: 2px 0; 
               }
               QSlider::handle:horizontal {
                   background-color: green; 
                   border: 1px solid #cccccc; 
                   width: 16px; 
                   margin: -7px 0; 
                   border-radius: 8px; 
               }
               """
            )
        else:
            self.light_brightness_slider.setEnabled(False)
            self.light_brightness_slider.setStyleSheet(
                """
                QSlider {
                    height: 20px; /* Height of the slider track */
                }
                QSlider::groove:horizontal {
                    background-color: #e0e0e0; 
                    border: 1px solid #cccccc;
                    height: 4px; 
                    margin: 2px 0;
                }
                QSlider::handle:horizontal {
                    background-color: gray; 
                    border: 1px solid #cccccc;
                    width: 16px; 
                    margin: -7px 0; 
                    border-radius: 8px; 
                }
                """
            )

        if self.thermostat and self.thermostat.status:

            self.thermostat_slider.setEnabled(True)
            self.thermostat_slider.setStyleSheet(
                """
               QSlider {
                   height: 20px; 
               }
               QSlider::groove:horizontal {
                   background-color: #e0e0e0; 
                   border: 1px solid #cccccc;
                   height: 4px; 
                   margin: 2px 0;
               }
               QSlider::handle:horizontal {
                   background-color: green; 
                   border: 1px solid #cccccc; 
                   width: 16px; 
                   margin: -7px 0;
                   border-radius: 8px;
               }
               """
            )
        else:

            self.thermostat_slider.setEnabled(False)
            self.thermostat_slider.setStyleSheet(
                """
                QSlider {
                    height: 20px; 
                }
                QSlider::groove:horizontal {
                    background-color: #e0e0e0; 
                    border: 1px solid #cccccc; 
                    height: 4px; 
                    margin: 2px 0; 
                }
                QSlider::handle:horizontal {
                    background-color: gray; 
                    border: 1px solid #cccccc; 
                    width: 16px;
                    margin: -7px 0; 
                    border-radius: 8px;
                }
                """
            )

        status_text = (
            f"Smart Light: {light_status} (Brightness: {light_brightness})\n"
            f"Thermostat: {thermostat_status} (Thermostat Temperature: {thermostat_temperature}℃)\n"
            f"Security Camera: {security_camera_status}\n"
            f"Security Status: {security_status}"
        )
        self.monitoring_text.setPlainText(status_text)

    def show_security_status(self):
        """Show the security status of the security camera."""
        if self.security_camera:
            self.security_camera.set_random_security_status()
            self.update_device_status()

