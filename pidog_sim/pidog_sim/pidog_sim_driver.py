import rclpy
from std_msgs.msg import Float32

HALF_DISTANCE_BETWEEN_WHEELS = 0.045
WHEEL_RADIUS = 0.025

class PiDogSimDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__motor_0 = self.__robot.getDevice('body_to_back_right_leg_b')
        self.__motor_1 = self.__robot.getDevice('back_right_leg_b_to_a')

        self.__motor_2 = self.__robot.getDevice('body_to_from_right_leg_b')
        self.__motor_3 = self.__robot.getDevice('front_right_leg_b_to_a')

        self.__motor_4 = self.__robot.getDevice('body_to_back_left_leg_b')
        self.__motor_5 = self.__robot.getDevice('back_left_leg_b_to_a')

        self.__motor_6 = self.__robot.getDevice('body_to_front_left_leg_b')
        self.__motor_7 = self.__robot.getDevice('front_left_leg_b_to_a')

        self.__motor_8 = self.__robot.getDevice('motor_8_to_tail')

        self.__motor_9 = self.__robot.getDevice('neck1_to_motor_9')
        self.__motor_10 = self.__robot.getDevice('neck2_to_motor_10')
        self.__motor_11 = self.__robot.getDevice('neck3_to_motor_11')
        
        self.__motor_0.setPosition(0)
        self.__motor_0.setVelocity(1.0)

        self.__motor_1.setPosition(0)
        self.__motor_1.setVelocity(1.0)

        self.__motor_2.setPosition(0)
        self.__motor_2.setVelocity(1.0)

        self.__motor_3.setPosition(0)
        self.__motor_3.setVelocity(1.0)

        self.__motor_4.setPosition(0)
        self.__motor_4.setVelocity(1.0)

        self.__motor_5.setPosition(0)
        self.__motor_5.setVelocity(1.0)

        self.__motor_6.setPosition(0)
        self.__motor_6.setVelocity(1.0)

        self.__motor_7.setPosition(0)
        self.__motor_7.setVelocity(1.0)

        self.__motor_8.setPosition(0)
        self.__motor_8.setVelocity(1.0)

        self.__motor_9.setPosition(0)
        self.__motor_9.setVelocity(1.0)

        self.__motor_10.setPosition(0)
        self.__motor_10.setVelocity(1.0)

        self.__motor_11.setPosition(0)
        self.__motor_11.setVelocity(1.)

        self.target_pos = 0

        rclpy.init(args=None)
        self.__node = rclpy.create_node('pidog_sim_driver')
        self.__node.create_subscription(
            Float32, 'motor_0_pos', self.__cmd_pos_callback, 1
        )

    def __cmd_pos_callback(self, msg: Float32):
        self.target_pos = float(msg.data)

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0.0)
        self.__motor_0.setPosition(self.target_pos)
