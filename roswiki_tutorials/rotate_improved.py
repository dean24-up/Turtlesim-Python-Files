#!/usr/bin/env python

#rotate_improved.py
#repeatedly prompts user to rotate the turtlebot through user input on speed and distance

#original rotate.py from http://wiki.ros.org/turtlesim/Tutorials/Rotating%20Left%20and%20Right and/or ttps://github.com/clebercoutof/turtlesim_cleaner 
#Last modified dean24-up 6/13/22

import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

def rotate():
    #Starts a new node
    rospy.init_node('robot_cleaner', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    repeat = input("Would you like to rotate the turtle?: ").strip().capitalize() #added
    while repeat == "True": #added
        # Receiving the user's input
        print("Let's rotate your robot")
        speed = float(input("Input your speed (degrees/sec):").strip()) #changed by SD
        angle = float(input("Type your distance (degrees):").strip())   #changed by SD
        clockwise = input("Clockwise?: ").strip().capitalize() #True or false, changed by SD

        #Converting from angles to radians
        angular_speed = speed*2*PI/360
        relative_angle = angle*2*PI/360

        #We wont use linear components
        vel_msg.linear.x=0
        vel_msg.linear.y=0
        vel_msg.linear.z=0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0

        # Checking if our movement is CW or CCW
        if clockwise == "True": #changed by SD
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)
        # Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_angle = 0

        while(current_angle < relative_angle):
            velocity_publisher.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t1-t0)

        #This was messing with my loop, I don't know what else commenting it out does though
        #Forcing our robot to stop
        #vel_msg.angular.z = 0
        #velocity_publisher.publish(vel_msg)
        #rospy.spin()
    
        repeat = input("Would you like to rotate the turtle?: ").strip().capitalize() #added
    print("Thanks for playing! Bye now :)")

if __name__ == '__main__':
    try:
        # Testing our function
        rotate()
    except rospy.ROSInterruptException:
        pass