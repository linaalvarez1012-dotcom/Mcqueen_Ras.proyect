
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_gz = FindPackageShare('mcqueen_gz_description')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='world_4.sdf',
        description='Archivo .sdf de la carpeta worlds/'
    )

    world_file = PathJoinSubstitution([
        pkg_gz,
        'worlds',
        LaunchConfiguration('world')
    ])

    xacro_file = PathJoinSubstitution([
        pkg_gz,
        'urdf',
        'mcqueen_gz.urdf.xacro'
    ])

    bridge_config = PathJoinSubstitution([
        pkg_gz,
        'config',
        'ros_gz_bridge.yaml'
    ])

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    # Publicador del estado del robot
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    # Iniciar Gazebo
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': ['-r ', world_file]
        }.items()
    )

    # Insertar el robot en Gazebo
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'mcqueen',
            '-x', '0',
            '-y', '-2',
            '-z', '0.2'
        ],
        output='screen'
    )

    # Puente ROS 2 - Gazebo usando el archivo YAML
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config
        }],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        rsp,
        gz_sim,
        spawn,
        bridge
    ])
