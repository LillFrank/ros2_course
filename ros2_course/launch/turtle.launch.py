from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtle1',
            output='screen',
        ),
        Node(
            package='ros2_course',
            executable='turtlesim_controller',
            name='turtlesim_controller',
            output='screen',
        ),

    ])
