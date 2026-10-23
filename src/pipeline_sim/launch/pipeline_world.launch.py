import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription

from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg = get_package_share_directory('pipeline_sim')
    world = os.path.join(pkg, 'worlds', 'pipeline.sdf')

    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r -v 3 {world}'}.items())

    m20_urdf = os.path.join(
        get_package_share_directory('m20_description'),
        'urdf',
        'M20.urdf',
    )

    spawn_m20 = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-world', 'pipeline_world',
                    '-file', m20_urdf,
                    '-name', 'M20',
                    '-x', '-1.5',
                    '-y', '0',
                    '-z', '0.7'
                ],
                output='screen',
            )
        ],
    )

    return LaunchDescription([gz, spawn_m20])