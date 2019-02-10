# TURTLEBOT LOCALIZATION AND NAVIGATION USING ROS!


The repository contains the work done as part of the Robotics module For master in computer vision and robotics " VIBOT", The Repository contains two different methods for autonomous  robots Localization and Navigation, [behavior_based](https://github.com/ElJAZRY/ROS_PROJECT/tree/master/behavior_based "behavior_based") and [map_based](https://github.com/ElJAZRY/ROS_PROJECT/tree/master/map_based "map_based") , the two methods represent different approaches to the problem of autonomous robots Localization and Navigation and a combination of both to get the benefits of both methods 


![Map based Vs Behavior-based navigation 1.](https://github.com/ElJAZRY/ROS_PROJECT/blob/master/behavior_based/map_behave.png)


Map based Vs Behavior-based navigation [1].


# ROS For TURTLEBOT

We use the ROS actionlib package to define simple action client, MoveBaseAction that communicate with the move_base package to preform our Navigation for one goal, the
move_base package implements an action server that accepts a goal pose for the robot (position
and orientation) and attempts to reach that goal by publishing Twist messages while monitoring
odometry and kinect scan data to avoid obstacles, also we use SMACH package to build state
machine that include the loading and unloading area as state for the robot to be in and move from
one area to another based on the state of the goal Robot .




![Move-Base](https://github.com/ElJAZRY/ROS_PROJECT/blob/master/behavior_based/Dlu_nav.png)


# SMACH 

SMACH is a task-level architecture for rapidly creating complex robot behavior , we use SMACH package based architecture to enable our robot to navigate through predefined points (Loading - Unloading) to preform the given scenario  . 

![Map based Vs Behavior-based navigation 1.](https://github.com/ElJAZRY/ROS_PROJECT/blob/master/behavior_based/projectDiagram.png)

# Dependency 

- ubuntu 14.04
- ROS Indigo
- rbx1  "ROS By Example Volume 1"
- rbx2  "ROS By Example Volume 2"


To Launch Map Based Navigation  :
```
roslaunch map_based.launch
 OR
python map_based/go_goal.py
```


To Launch Behavior Based Navigation  :
```
roslaunch behavior_based.launch
 OR
python behavior_based/wander.py
```


[![DEMO](https://github.com/ElJAZRY/ROS_PROJECT/blob/master/behavior_based/snapshot.jpg)](https://youtu.be/BLybKmHQiwA "DEMO")



[1] Introduction to Autonomous Mobile Robots, {Roland Siegwart, Illah Reza Nourbakhsh, Davide Scaramuzza}
