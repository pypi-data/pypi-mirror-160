import serial

class XCtrl:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
        )
        self.ser.close()
        self.ser.open()

    def ping_controller(self):
        self.serial_send("pin")
        data = self.ser.readline().decode("utf-8")[:-2]
        return data


    def set_limit(self, limit_name: str, limit_value: float):
        available_limit_names = ["current", "velocity", "undervoltage", "overvoltage"]
        if not limit_name in available_limit_names:
            # TODO: raise some warnings  
            return

        template = "set_limi_{}_{}"
        self.serial_send(template.format(limit_name[:3], limit_value))

    def set_torque_constant(self, motor_torque_constant: float):
        template = "set_torc_{}"
        self.serial_send(template.format(motor_torque_constant))

    def set_poles(self, motor_num_poles_pairs: int):
        template = "set_pole_{}"
        self.serial_send(template.format(motor_num_poles_pairs))

    def set_encoder_ppr(self, encoder_ppr: float):
        template = "set_eppr_{}"
        self.serial_send(template.format(encoder_ppr))

    def set_mode(self, mode: str):
        available_modes = ['position', 'velocity', 'torque']

        if not limit_name in available_modes:
            # TODO: raise some warnings  
            return

        template = "set_mode_{}"
        self.serial_send(template.format(mode[:3]))

    def calibrate(self):
        self.serial_send("cal")

    def set_position(self, position: float):
        template = "inp_pos_{}"
        self.serial_send(template.format(position))

    def set_velocity(self, velocity: float):
        template = "inp_vel_{}"
        self.serial_send(template.format(velocity))

    def set_torque(self, torque: float):
        template = "inp_tor_{}"
        self.serial_send(template.format(torque))


    def serial_send(self, command_string: str):
        self.ser.write(bytes(command_string, 'utf-8'))