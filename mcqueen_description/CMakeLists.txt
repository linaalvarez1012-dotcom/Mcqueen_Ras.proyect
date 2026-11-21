cmake_minimum_required(VERSION 3.8)
project(mcqueen_description)

find_package(ament_cmake)

install(
    DIRECTORY config launch rviz urdf meshes
    DESTINATION share/${PROJECT_NAME}/
)

ament_package()