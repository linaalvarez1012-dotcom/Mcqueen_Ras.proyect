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
        description='Archivo .sdf de la carpeta worlds/ que se va a cargar'
    )

    world_file = PathJoinSubstitution([
        pkg_gz, 'worlds', LaunchConfiguration('world')
    ])

    xacro_file = PathJoinSubstitution([pkg_gz, 'urdf', 'mcqueen_gz.urdf.xacro'])
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str
    )

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
        launch_arguments={'gz_args': ['-r ', world_file]}.items()
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                    '-name', 'mcqueen',
                    '-x', '0', '-y', '-2', '-z', '0.2'],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
        ],
        output='screen'
    )

    return LaunchDescription([world_arg, rsp, gz_sim, spawn, bridge])