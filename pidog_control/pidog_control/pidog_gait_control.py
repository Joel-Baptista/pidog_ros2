from math import sin, cos, pi
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

L1 = 0.047 # meters
L2 = 0.0635
W = 0.0095


class PiDogGaitControl(Node):

    def __init__(self):
        super().__init__("pidog_gait_control")

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, "motor_pos", qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.timer = self.create_timer(1 / 30, self.update)

        self.sit = [] 
        
        for a in [30, 60, -30, -60, 80, -45, -80, 45]:
            self.sit.append(a * (pi / 180))

        # message declarations
        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = "odom"
        self.odom_trans.child_frame_id = "axis"
        self.joint_state = JointState()

        self.get_logger().info("{0} started".format(self.get_name()))

    def update(self):
        # update joint_state
        now = self.get_clock().now()
        self.joint_state.header.stamp = now.to_msg()
        self.joint_state.name = [
            "motor_0",
            "motor_1",
            "motor_2",
            "motor_3",
            "motor_4",
            "motor_5",
            "motor_6",
            "motor_7",
            "motor_8",
            "motor_9",
            "motor_10",
            "motor_11",
        ]
        self.joint_state.position = [
            self.sit[0],
            self.sit[1],
            self.sit[2],
            self.sit[3],
            self.sit[4],
            self.sit[5],
            self.sit[6],
            self.sit[7],
            0.0,
            0.0,
            0.0,
            0.0,
        ]

        # send the joint state and transform
        self.joint_pub.publish(self.joint_state)


def main():
    try:
        with rclpy.init():
            node = PiDogGaitControl()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
