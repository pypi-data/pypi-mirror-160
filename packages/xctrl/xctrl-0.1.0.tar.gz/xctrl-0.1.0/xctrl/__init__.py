"""
Library for X Controller by Precision Robotics.
"""
from .xctrl import XCtrl
import serial
import serial.tools.list_ports


__version__ = "0.1.0"
__author__ = "Precision Robotics"

manufacturer = "Arduino LLC"

found_objects = []


def scan():
    xcontrol_ports = find_xcontroller_ports()
    exist_ports = [o.port for o in found_objects]
    for p in xcontrol_ports:
        if not p.device in exist_ports:
            found_objects.append(XCtrl(p.device))
    return found_objects


def find_xcontroller_ports():
    found_xcontrol_ports = []
    for port in serial.tools.list_ports.comports():
        if is_usb_serial(port) and port.manufacturer == manufacturer:
            found_xcontrol_ports.append(port)
    return found_xcontrol_ports


def is_usb_serial(port):
    """Checks device to see if its a USB Serial device.
    The caller already filters on the subsystem being 'tty'.
    """
    if port.vid is None:
        return False
    return True