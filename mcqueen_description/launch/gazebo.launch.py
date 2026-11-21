from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('mcqueen_description')

    xacro_file = PathJoinSubstitution([pkg, 'urdf', 'mcqueen.urdf.xacro'])
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str
    )

    # Publica /robot_description y TF
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description,
                        'use_sim_time': True}],
        output='screen'
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
        ])),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    # Crea el robot dentro de Gazebo a partir de /robot_description
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                    '-name', 'mcqueen',
                    '-z', '0.05'],
        output='screen'
    )

    return LaunchDescription([rsp, gz_sim, spawn])