#!/usr/bin/env python

#cool_s_drawer.py
#draws a cool s once booted up. I wrote this because I thought it would be fun and I wanted to see if I could
#piece together some basic turtlesim coding using the examples I've done.

#I understand all but the syst import. From move_turtle_get_pose.py
import rospy
from geometry_msgs.msg import Twist
#from turtlesim.msg import Pose <-- dunno if I need this, for position tracking
import syst

#global variables
vel = Twist() #variable that encompasses linear and angular velocity

#Initialize the node
rospy.init_node('cool_s', anonymous=True)
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
rate = rospy.Rate(10) #10 hz

#main function that draws the s
def draw_s():

    move_turt(1, 45, 2)

    #Twist setup
    #to see the data fields associated with Twist, run:
    #rosmsg show geometry_msgs Twist
    

#takes linear x, angular z, and distance as parameters, all other Twist fields are 0 for turtlesim purposes
#this is more or less copiedd from move.py, I'm just making a separate function
def move_turt(lin_vel, ang_vel, distance):
    vel.linear.x = lin_vel #speed arbitrary unless turtle should rotate in place
    vel.linear.y = 0
    vel.linear.z = 0

    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = ang_vel

    #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    #This is from move.py. It's essentially taking the speed times the time difference
    #to determine how far you've gone and whether to continue going
    while(current_distance < distance):
        #Publish velocity
        velocity_publisher.publish(vel)
        #Takes actual time to velocity calculus
        t1 = rospy.Time.now().tosec()
        #Calculates distancePoseStamped
        current_distance = speed*(t1-t0)
    
    #stop the turtle
    vel.linear.x = 0
    velocity_publisher.publish(vel)
   

#I wonder if you can call a service within a script like this? Because ideally
#the turtle would be reset upon call, but I don't know if I can put that as 
#part of this program easily


if __name__ == '__main__':
    try:
        #Testing our function
        draw_s()
    except rospy.ROSInterruptException: pass
