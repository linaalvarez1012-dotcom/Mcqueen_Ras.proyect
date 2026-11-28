# Mcqueen_Ras.proyect
![ROS2](https://img.shields.io/badge/ROS2-Jazzy-22314E?logo=ros&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-F58113)
![RViz](https://img.shields.io/badge/RViz-2-4285F4)

McQueen is a differential-drive mobile robot developed as a hands-on learning project for ROS 2 Jazzy. It has two independently driven wheels, a passive caster wheel, a chassis, and a simulated 2D LiDAR sensor.

The project began with robot visualization in RViz 2, using URDF (Unified Robot Description Format) and Xacro to define the robot's geometry, dimensions, materials, and joints. It then progressed to Gazebo Harmonic, where collision geometries, masses, inertial properties, differential-drive motion, and simulated worlds can be tested. Finally, the navigation package introduces SLAM Toolbox for 2D mapping and provides a starting point for future EasyNav navigation.

---
## Team members 

Juan Sebastian Moya Perdomo

Lina Sofia Alvarez Martinez

---

## Software

* Ubuntu 24.04
* Ros 2 Jazzy
* Python
* C++
* URDF/Xacro
* ROS 2 Teleoperation (Teleop)
* Git & GitHub
* Rviz 2
* Gazebo Harmonic
* SDF
* SLAM Toolbox

---

# Step by step

## Rviz visualization

We first created McQueen using primitive geometries such as boxes, cylinders, and spheres. Each component was positioned using its dimensions and origin relative to the robot's main coordinate frame.

The model was then organized into separate Xacro macros for the chassis, driven wheels, caster wheel, wheel track, materials, and laser sensor. The main  `mcqueen.urdf.xacro` file assembles these components and connects them through joints. RViz 2 is used to inspect the model and its coordinate frames before simulation.


## Gazebo

The same robot description is used as the starting point for Gazebo simulation. Collision geometries, masses, and inertia tensors allow the simulated robot to interact with the environment. A differential-drive system provides a way to test wheel-based motion.

We also created practice environments using SDF (Simulation Description Format), including ground planes, lights, and obstacle boxes. Additional worlds support experiments with obstacle detection and navigation.


## LiDar and Mapping

The laser link is configured as a simulated GPU LiDAR in Gazebo. In the supplied model, it scans approximately 360° with 720 horizontal samples and a nominal range of 0.08–10 m at 10 Hz.

Laser scans can be bridged from Gazebo to ROS 2 using `ros_gz_bridge` and visualized in RViz through `/scan`. The `mc_navigation}`  package contains the SLAM Toolbox launch, YAML parameters, RViz configuration, and a directory for generated maps. SLAM requires valid odometry and TF transforms in addition to laser measurements.

---

# Installation and setup

## 1. Create a ROS2 workspace

```bash
mkdir -p ~/RAS_Junior2/RasJ2_ws/src
cd ~/RAS_Junior2/RasJ2_ws/src

```
This command requires `src` to be empty. If you already have a workspace with files in `src`, clone into a separate directory and copy or link only the needed packages instead.

## 2. Build the workspace


```bash
cd ~/RAS_Junior2/RasJ2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash

```
Run `source`  `~/RAS_Junior2/RasJ2_ws/install/setup.bash`  in each new terminal used for this workspace.


## 3. Run the proyect

```bash
source /opt/ros/jazzy/setup.bash
source ~/RAS_Junior2/RasJ2_ws/install/setup.bash

```

## 4. Visualize McQueen in RViz 2

```bash
ros2 launch mcqueen_description display.launch.py

```

## 5. Simulate McQueen in Gazebo Harmonic

```bash
ros2 launch mcqueen_gz_description mcqueen_gazebo.launch.py world:=world_4.sdf

```
To select another supplied world, replace `world_4.sdf` with `world_1.sdf`, `wrld_2.sdf`, or `world_3.sdf` .

The `world:=...` argument applies to the updated McQueen launch file, not to the older version that references   `jackal_gazebo` and uses `world_name` . Confirm the code in your local branch before running it.

## 6. Start SLAM Toolbox

```bash
ros2 launch mc_navigation slam.launch.py

```
In a separate terminal:
```bash
ros2 run rviz2 rviz2 -d \
  ~/RAS_Junior2/RasJ2_ws/src/mc_navigation/rviz/slam.rviz
```

The mapping view subscribes to `/scan` and `/map` and uses `map` as its fixed frame. For mapping to work, the TF chain must include:

Use the `/map` display in RViz to watch the map develop as the robot moves. This is an integration workflow, not proof that SLAM or autonomous navigation has already been validated in the current branch.

## 7. Keyboard teleoperation

Once the differential-drive command path is working, publish velocity commands with:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap cmd_vel:=/cmd_vel

```
This requires the bridge and Gazebo differential-drive plugin to agree on the command topic and message type. If the robot does not move, inspect the actual `/cmd_vel` topic and the Gazebo bridge rather than changing the robot geometry.

---

## Video 


--- 

<div align="center">McQueen — From robot description to simulated navigation.
</div>
