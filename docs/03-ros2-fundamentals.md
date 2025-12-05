---
id: ros2-fundamentals
title: ROS 2 Fundamentals
sidebar_position: 3
---

# ROS 2 Fundamentals

## Overview

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It provides tools and libraries for building robot applications across a wide variety of robotic platforms.

## Core Concepts

### Nodes

Nodes are executable processes in ROS 2. They communicate with each other to form a robot's computational graph.

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Node started')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Topics

Topics are named buses over which nodes exchange messages. A node can publish to or subscribe to a topic.

```python
from std_msgs.msg import String

# Publisher
publisher = node.create_publisher(String, 'topic_name', 10)
msg = String()
msg.data = 'Hello World'
publisher.publish(msg)

# Subscriber
def callback(msg):
    print(f'Received: {msg.data}')

subscription = node.create_subscription(String, 'topic_name', callback, 10)
```

### Services

Services allow synchronous request-response communication between nodes.

```python
from example_interfaces.srv import AddTwoInts

def add_callback(request, response):
    response.sum = request.a + request.b
    return response

service = node.create_service(AddTwoInts, 'add_two_ints', add_callback)
```

### Actions

Actions provide a framework for preemptable, long-running tasks.

```python
from rclpy_action import ActionServer
from example_interfaces.action import Fibonacci

action_server = ActionServer(
    node,
    Fibonacci,
    'fibonacci',
    execute_callback
)
```

## URDF (Unified Robot Description Format)

URDF is an XML format to describe a robot's kinematic and dynamic properties.

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <link name="base_link">
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>
  <link name="right_leg"/>
  <joint name="right_leg_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_leg"/>
    <axis xyz="0 1 0"/>
  </joint>
</robot>
```
