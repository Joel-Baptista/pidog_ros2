from math import sin, cos, pi
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

import numpy as np
import time
from pidog_control.kinemactics import leg_inverse_kin, straight_walk_planner, four_legs_inverse_kin, pivot_planner

import copy

INIT_X = 0.0
INIT_Y = 0.08
FPS = 1 / 10


class PiDogGaitControl(Node):

    def __init__(self):
        super().__init__("pidog_gait_control")

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, "motor_pos", qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.create_subscription(
            JointState, "joint_states", self.joint_states_callback, 1
        )


        x = np.array([0.02, 0.02, -0.01, -0.01])
        y = np.ones((4,)) * INIT_Y
        leg_sides = np.array([True, False, True, False])
        angles = four_legs_inverse_kin(x, y, leg_sides)

        self.init_angles = angles

        self.init_angles.extend([0.0, 0.0, 0.0, 0.0])

        print("Init angles: ", self.init_angles)

        # message declarations
        self.odom_trans = TransformStamped()
        self.odom_trans.header.frame_id = "odom"
        self.odom_trans.child_frame_id = "axis"
        self.joint_state = JointState()

        self.get_logger().info("{0} started".format(self.get_name()))

        self.current_joint_states = [0.0] * 12

        time.sleep(3)

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
        self.joint_state.position = self.init_angles

        # send the joint state and transform
        self.joint_pub.publish(self.joint_state)

        self.timer = self.create_timer(FPS, self.update)

        self.angle_counter = 0
        self.planned_angles = pivot_planner(INIT_X, INIT_Y)
        self.angle_number = len(self.planned_angles)


        # self.planned_angles = leg_circle_path(self.sit[0], self.sit[1], self.angle_number, 0.01, True)

    def joint_states_callback(self, msg):

        self.current_joint_states = msg.position

    def update(self):

        ang_counter = self.angle_counter % self.angle_number
        self.angle_counter += 1

        joint_state = JointState()

        now = self.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        joint_state.name = [
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

        if ang_counter == 0:
            joint_state.position = self.init_angles
        else:    
            joint_state.position = self.planned_angles[ang_counter - 1]

        self.joint_pub.publish(joint_state)


def main():
    try:
        with rclpy.init():
            node = PiDogGaitControl()
            rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == "__main__":
    main()
