---
id: digital-twin-simulation
title: Digital Twin Simulation
sidebar_position: 4
---

# Digital Twin Simulation

## Introduction to Digital Twins

A digital twin is a virtual replica of a physical robot that enables testing, training, and validation in simulation before deploying to hardware. Digital twins bridge the gap between design and reality.

### Benefits of Simulation

- **Cost Reduction**: Develop and test without expensive hardware
- **Safety**: Train control algorithms without risk to real robots
- **Scalability**: Run multiple simulations in parallel
- **Repeatability**: Create deterministic test scenarios
- **Iteration Speed**: Rapid prototyping and refinement

## Gazebo Simulation Framework

Gazebo is an open-source robotics simulator that integrates with ROS 2.

### Gazebo Components

```bash
# Install Gazebo
sudo apt-get install ros-humble-gazebo-ros

# Launch a simulation
ros2 launch gazebo_ros gazebo.launch.py
```

### World Files (SDF Format)

```xml
<?xml version='1.0'?>
<sdf version='1.10'>
  <world name='default_world'>
    <physics name='default_physics' default='true' type='ode'/>
    <plugin name='ignition::gazebo::Systems::Physics' filename='libignition-gazebo-physics-system.so'/>

    <light name='sun' type='directional'>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name='ground_plane'>
      <static>true</static>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
      </link>
    </model>
  </world>
</sdf>
```

## Physics Simulation

### Key Physics Parameters

- **Gravity**: Typically 9.81 m/s² downward
- **Surface Friction**: Affects robot-ground interaction
- **Damping**: Energy dissipation in joints and links
- **Time Step**: Resolution of physics calculation (usually 0.001s)

### Robot Dynamics

```python
import numpy as np

class RobotDynamics:
    def __init__(self, mass, inertia, gravity=9.81):
        self.mass = mass
        self.inertia = inertia
        self.gravity = gravity

    def compute_torques(self, joint_angles, joint_velocities, accelerations):
        """Compute required torques using inverse dynamics"""
        # Gravity compensation
        g_torques = self.gravity_torques(joint_angles)

        # Inertial effects
        i_torques = self.inertia_torques(accelerations)

        # Friction compensation
        f_torques = self.friction_torques(joint_velocities)

        return g_torques + i_torques + f_torques

    def gravity_torques(self, joint_angles):
        # Compute torques needed to counteract gravity
        pass

    def inertia_torques(self, accelerations):
        # Compute torques from acceleration
        return self.inertia @ accelerations

    def friction_torques(self, velocities):
        # Compute friction compensation
        damping = 0.1
        return -damping * velocities
```

## Isaac Sim

Isaac Sim is NVIDIA's advanced simulation platform with advanced physics, vision, and AI training capabilities.

### Isaac Sim Features

- **RTX-Enabled Physics**: Photorealistic rendering and accurate physics
- **Sensor Simulation**: RGB-D cameras, LiDAR, contact sensors
- **Domain Randomization**: Automatically vary simulation parameters for robust training
- **ROS 2 Integration**: Native support for ROS 2 communication
- **RL Training**: Built-in reinforcement learning framework

### Python API Example

```python
from omni.isaac.kit import SimulationApp

# Initialize simulator
simulation_app = SimulationApp({"headless": False})

# Create stage and load robot
from omni.isaac.core.world import World
world = World(stage_units_in_meters=1.0)

# Add robot from URDF
from omni.isaac.core.utils.stage import add_reference_to_stage
robot = add_reference_to_stage(
    usd_path="/path/to/robot.usd",
    prim_path="/World/robot"
)

# Simulation loop
while simulation_app.is_running():
    world.step(render=True)

simulation_app.close()
```

## Sensor Simulation

### RGB-D Camera Simulation

```python
from omni.isaac.sensor import Camera

camera = Camera(
    prim_path="/World/camera",
    position=(0, 0, 1),
    resolution=(640, 480),
    rgb=True,
    depth=True
)

# Get sensor data
rgb = camera.get_rgb()
depth = camera.get_depth()
```

### LiDAR Simulation

```python
from omni.isaac.sensor import LiDAR

lidar = LiDAR(
    prim_path="/World/lidar",
    position=(0, 0, 0.5),
    rotation=(0, 0, 0),
    min_range=0.1,
    max_range=100.0,
    channels=64,
    horizontal_fov=360,
    vertical_fov=30
)

point_cloud = lidar.get_point_cloud()
```

## Testing in Simulation

### Unit Tests for Controllers

```python
import unittest
from robot_controller import BalanceController

class TestBalanceController(unittest.TestCase):
    def setUp(self):
        self.controller = BalanceController()

    def test_zero_moment_point(self):
        # Simulate robot standing
        joint_angles = np.zeros(12)
        zmp = self.controller.compute_zmp(joint_angles)

        # ZMP should be near center of support polygon
        self.assertAlmostEqual(zmp[0], 0.0, places=2)
        self.assertAlmostEqual(zmp[1], 0.0, places=2)

    def test_stability_margin(self):
        # Test stability with external perturbation
        joint_angles = np.array([0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        margin = self.controller.stability_margin(joint_angles)

        self.assertGreater(margin, 0.01)
```

## Closing the Sim-to-Real Gap

### Domain Randomization

```python
import random

def randomize_simulation():
    """Vary simulation parameters to improve real-world robustness"""

    # Randomize mass
    mass_scale = random.uniform(0.9, 1.1)

    # Randomize friction
    friction = random.uniform(0.5, 1.5)

    # Randomize damping
    damping = random.uniform(0.05, 0.2)

    return {
        "mass_scale": mass_scale,
        "friction": friction,
        "damping": damping
    }
```

### Transfer Learning

```python
class SimToRealController:
    def __init__(self):
        # Train in simulation
        self.sim_policy = self.train_in_simulation()

    def train_in_simulation(self):
        # Use domain randomization
        policies = []
        for _ in range(100):
            params = randomize_simulation()
            policy = self.train_policy(params)
            policies.append(policy)
        return self._ensemble_policy(policies)

    def _ensemble_policy(self, policies):
        # Average policies from multiple randomized simulations
        def policy(state):
            actions = [p(state) for p in policies]
            return np.mean(actions, axis=0)
        return policy
```
