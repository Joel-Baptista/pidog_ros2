import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController
from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    package_dir = get_package_share_directory('pidog_sim')
    robot_description_path = os.path.join(package_dir, 'resource', 'pidog_world.urdf')

    with open(robot_description_path, 'r') as f:
        robot_description_text = f.read()

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'pidog_world.wbt')
    )

    my_robot_driver = WebotsController(
        robot_name='PiDog',
        parameters=[
            {'robot_description': robot_description_path},
        ]
    )

    controller_after_webots = RegisterEventHandler(
        OnProcessStart(
            target_action=webots,
            on_start=[TimerAction(period=2.0, actions=[my_robot_driver])]
        )
    )

    return LaunchDescription([
        webots,
        controller_after_webots,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])