#!/usr/bin/env python
#same as move.py, but prompts user to move turtle again until told not to.
#I added the while loop where I thought it would make sense, without really
#knowing how it might affect ROS. It seems to work, but I had to comment out
#the shutdown line.

#Last modified dean24-up 6/13/22
#original from http://wiki.ros.org/turtlesim/Tutorials/Moving%20in%20a%20Straight%20Line

import rospy
from geometry_msgs.msg import Twist

def move():
    # Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #added, used for while loop
    repeat = input("Would you like to move the turtle?: ").strip().capitalize() #True or False

    #loops as many times until doesn't want to move robot anymore.
    while repeat == "True": 
        #Receiving the user's input
        print("Let's move your robot")
        speed = int(input("Input your speed:").strip())
        distance = int(input("Type your distance:").strip())
        isForward = input("Forward?: ").strip().capitalize()#True or False

        #Checking if the movement is forward or backwards
        if(isForward == "True"):
            vel_msg.linear.x = abs(speed)
        else:
            vel_msg.linear.x = -abs(speed)
        #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0

        #while not rospy.is_shutdown(): commenting this out just to see

        #Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        #Loop to move the turtle in an specified distance
        while(current_distance < distance):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
            current_distance= speed*(t1-t0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)

        repeat = input("Would you like to move the turtle?: ").strip().capitalize() #True or False

    print("Thanks for playing! Bye now :)") #added

if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass