#!/usr/bin/env python

#cool_s_drawer.py
#draws a cool s once booted up. I wrote this because I thought it would be fun and I wanted to see if I could
#piece together some basic turtlesim coding using the examples I've done.

#this is kinda messy cuz I made it in vim and it doesnt use Pos, it just uses
# time stuff. Thus, it doesn't get the angle right every time. So it looks like I'm
#gonna have to use Pos and a subscriber and figure out how to read those values.
#I'm commiting for now and coming back to fix it later

#I understand all but the syst import. From move_turtle_get_pose.py
import rospy
from geometry_msgs.msg import Twist
#from turtlesim.msg import Pose <-- dunno if I need this, for position tracking
#import syst

#global variables
vel = Twist() #vairiable that encompasses linear and angular velocity
PI = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482

#main function that draws the s
def draw_s():

    rotate_turt(90)
    move_turt(2, 1)
    move_turt(-2, 1)

    rotate_turt(45)
    move_turt(2, 1)
    
    rotate_turt(55)
    move_turt(2,1.75)

    rotate_turt(45)
    move_turt(2, 1)


    #Twist setup
    #to see the data fields associated with Twist, run:
    #rosmsg show geometry_msgs Twist
    

#takes linear x  and distance as parameters, all other Twist fields are 0 for turtlesim purposes
#this is more or less copied from move.py, I'm just making a separate function

#rotates the turtle without moving it
def rotate_turt(relative_angle):
    relative_angle = relative_angle*2*PI/360 #conversion from degrees to radians
    ang_vel = 40 #ang_vel in degrees/sec
    ang_vel = ang_vel*2*PI/360
    
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = ang_vel

    #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    #rotate turtle until matches correct angle
    while (current_angle <= relative_angle):
       velocity_publisher.publish(vel)
       t1 = rospy.Time.now().to_sec()
       current_angle = ang_vel*(t1-t0)
    vel.linear.z = 0

def move_turt(lin_vel,distance):
    
    vel.linear.x = lin_vel #speed arbitrary unless turtle should rotate in place
    vel.linear.y = 0
    vel.linear.z = 0

    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = 0

    #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    #This is from move.py. It's essentially taking the speed times the time difference
    #to determine how far you've gone and whether to continue going
    while(current_distance < distance):
        #Publish velocity
        velocity_publisher.publish(vel)
        #Takes actual time to velocity calculus
        t1 = rospy.Time.now().to_sec()
        #Calculates distancePoseStamped
        current_distance = lin_vel*(t1-t0)
    
    #stop the turtle
    vel.linear.x = 0
    velocity_publisher.publish(vel)
   

#I wonder if you can call a service within a script like this? Because ideally
#the turtle would be reset upon call, but I don't know if I can put that as 
#part of this program easily


if __name__ == '__main__':
    try:
        #Testing our function
        #Initialize the node
        rospy.init_node('cool_s', anonymous=True)
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        #rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
        rate = rospy.Rate(10) #10 hz
        draw_s()
    except rospy.ROSInterruptException: pass
