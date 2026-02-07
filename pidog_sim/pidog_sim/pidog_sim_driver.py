import rclpy
from std_msgs.msg import Float32, Float32MultiArray
from rclpy.qos import QoSProfile
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
import copy

MOTOR_MAPPING = {
    "motor_0": 0,
    "motor_1": 1,
    "motor_2": 2,
    "motor_3": 3,
    "motor_4": 4,
    "motor_5": 5,
    "motor_6": 6,
    "motor_7": 7,
    "motor_8": 8,
    "motor_9": 9,
    "motor_10": 10,
    "motor_11": 11,
}


class PiDogSimDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__motor_0 = self.__robot.getDevice("body_to_front_left_leg_b")
        self.__motor_1 = self.__robot.getDevice("front_left_leg_b_to_a")

        self.__motor_2 = self.__robot.getDevice("body_to_front_right_leg_b")
        self.__motor_3 = self.__robot.getDevice("front_right_leg_b_to_a")

        self.__motor_4 = self.__robot.getDevice("body_to_back_left_leg_b")
        self.__motor_5 = self.__robot.getDevice("back_left_leg_b_to_a")

        self.__motor_6 = self.__robot.getDevice("body_to_back_right_leg_b")
        self.__motor_7 = self.__robot.getDevice("back_right_leg_b_to_a")

        self.__motor_8 = self.__robot.getDevice("motor_8_to_tail")

        self.__motor_9 = self.__robot.getDevice("neck1_to_motor_9")
        self.__motor_10 = self.__robot.getDevice("neck2_to_motor_10")
        self.__motor_11 = self.__robot.getDevice("neck3_to_motor_11")

        self.motor_list = [
            self.__motor_0,
            self.__motor_1,
            self.__motor_2,
            self.__motor_3,
            self.__motor_4,
            self.__motor_5,
            self.__motor_6,
            self.__motor_7,
            self.__motor_8,
            self.__motor_9,
            self.__motor_10,
            self.__motor_11,
        ]

        # Safety: set a non-zero speed for position control
        for m in self.motor_list:
            if m is None:
                raise RuntimeError(
                    "Missing motor device — check names in the PROTO/WBT."
                )
            # m.setVelocity(1.0)
            m.setPosition(0.0)

        self.joint_states = None
        self.joint_names = None

        self.joint_states_belief = [0.0] * 12
        self.motor_names = list(MOTOR_MAPPING.keys())

        rclpy.init(args=None)
        self.__node = rclpy.create_node("pidog_sim_driver")
        # Create subscription on the existing node (NO rclpy.init, NO extra node)
        self.__node.create_subscription(
            JointState, "motor_pos", self.__cmd_pos_callback, 1
        )

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.__node.create_publisher(
            JointState, "joint_states", qos_profile
        )
        self.broadcaster = TransformBroadcaster(self.__node, qos=qos_profile)
        self.timer = self.__node.create_timer(1 / 30, self.update_states)

        self.__node.get_logger().info("PiDogSimDriver initialized.")

    def update_states(self):

        joint_state = JointState()

        now = self.__node.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        joint_state.name = self.motor_names
        joint_state.position = self.joint_states_belief

        self.joint_pub.publish(joint_state)

    def __cmd_pos_callback(self, msg: Float32):
        self.joint_states = msg.position
        self.joint_names = msg.name

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)
        # The driver spins the executor; just apply your control here


        if not (self.joint_states is None or self.joint_names is None):

            joints = copy.deepcopy(self.joint_states)
            names = copy.deepcopy(self.joint_names)

            for i, n in enumerate(names):
                idx = MOTOR_MAPPING[n]
                self.motor_list[idx].setPosition(joints[i])
                self.joint_states_belief[idx] = joints[i]
