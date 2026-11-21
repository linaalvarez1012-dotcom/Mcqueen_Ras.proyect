from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='true',
        choices=['true', 'false'],
        description='Flag to enable joint_state_publisher_gui'
    )

    # Ruta RELATIVA dentro del paquete
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value='urdf/mcqueen.urdf',
        description='URDF path relative to the package share directory'
    )

    display_launch = IncludeLaunchDescription(
        PathJoinSubstitution([
            FindPackageShare('urdf_launch'),
            'launch',
            'display.launch.py'
        ]),
        launch_arguments={
            'urdf_package': 'mcqueen_description',
            'urdf_package_path': LaunchConfiguration('model'),
            'jsp_gui': LaunchConfiguration('gui'),
        }.items()
    )

    return LaunchDescription([gui_arg, model_arg, display_launch])