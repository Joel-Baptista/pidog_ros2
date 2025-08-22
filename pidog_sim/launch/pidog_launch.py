import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController
from launch.actions import RegisterEventHandler, TimerAction, LogInfo
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node

def generate_launch_description():
    package_dir = get_package_share_directory('pidog_sim')
    world_description_path = os.path.join(package_dir, 'resource', 'pidog_world.urdf')
    robot_description_path = os.path.join(package_dir, 'resource', 'pidog_world.urdf')

    with open(robot_description_path) as f:
        robot_description = f.read()


    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'pidog_world.wbt'),

    )

    my_robot_driver = WebotsController(
        robot_name='PiDog',
        parameters=[
            {'robot_description': world_description_path},
        ],
    )

    return LaunchDescription([
        webots,
        my_robot_driver,
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': True, 'robot_description': robot_description}],
            arguments=[robot_description]),
        Node(
            package='pidog_control',
            executable='pidog_gait_control',
            name='pidog_gait_control',
            output='screen'),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])