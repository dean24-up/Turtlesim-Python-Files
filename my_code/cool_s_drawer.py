#!/usr/bin/env python

#cool_s_drawer.py
#draws a cool s once booted up. I wrote this because I thought it would be fun and I wanted to see if I could
#piece together some basic turtlesim coding using the examples I've done.

#update using Pose data for angle calculations. Not sure if this will work.

#I understand all but the syst import. From move_turtle_get_pose.py
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose 
import sys

#global variables
vel = Twist() #vairiable that encompasses linear and angular velocity
#pos = Pose() #variable that encompasses Turtle's pose
PI = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482
turtle_theta = 0.0
SPEED = 2
ANG_SPEED = 40

#main function that draws the s
def draw_s():

    rotate_turt(88.5)
    move_turt(SPEED, 1)
    move_turt(-SPEED, 1)
        
    rotate_turt(45)
    move_turt(SPEED, 1)

    rotate_turt(88.5)
    move_turt(SPEED, 1)

    rotate_turt(88.5+45)
    move_turt(SPEED, 1)

    rotate_turt(-45)
    move_turt(SPEED, 1)

    #rotate_turt(45)
    #move_turt(2, 1)
    
    #rotate_turt(55)
    #move_turt(2,1.75)

    #rotate_turt(45)
    #move_turt(2, 1)


#takes linear x  and distance as parameters, all other Twist fields are 0 for turtlesim purposes
#this is more or less copied from move.py, I'm just making a separate function

def pose_callback(pose):
    global turtle_theta
    rospy.loginfo("Turtle_Theta = %f\n", pose.theta)
    turtle_theta = pose.theta

#takes angle in radians and checks caes 
def return_case(start_angle, end_angle):
    start_angle = start_angle * 180 /PI #convert to degrees
    if start_angle > 0 and (start_angle < 180):
        if end_angle > 0 and (end_angle < 180):
            return 1                            #case 1, both angles positive
        else:
            return 2                            #case 2, start positive end negative  
    elif angle < 0 and (angle > -180):
        if end_angle > 0 and (start_angle < 180):
            return 3                            #case 3, start negative, end negative
        else:
            return 4

#rotates the turtle without moving it
def rotate_turt(final_angle):
    
    final_angle = final_angle*PI/180 #conversion from degrees to radians
    starting_angle = turtle_theta

    if starting_angle < 0:
        starting_angle = starting_angle + 2*PI
    if final_angle < 0:
        final_angle = final_angle + 2*PI

    #ADD, if starting angle > final angle then ang_vel = -ANG_SPEED
    if starting_angle < final_angle:
        ang_vel = ANG_SPEED
    else:
        ang_vel = -ANG_SPEED

    #Then farther below change the conditions for the while loop
    ang_vel = ang_vel*2*PI/360

    #Twist setup
    #to see the data fields associated with Twist, run:
    #rosmsg show geometry_msgs Twist
    vel.linear.x = 0
    vel.linear.y = 0
    vel.linear.z = 0
    
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = ang_vel

    #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    
    #rotate turtle until matches correct angle

    #while the current position of the turtle is less than the difference
    #between the original angle and the final angle (the difference is the
    # relative angle), keep moving
    
    #if return_case(starting_angle, final_angle) == 1:
    #    if starting angle < final angle:
    #        while turtle_theta < (final_angle):
    #            velocity_publisher.publish(vel)
    #    else:
    #        while turtle_theta > final_angle:
    #            velocity_publisher.publish(vel)
    #if return_case(starting_angle, final_angle) == 2:
    #    if final_angle
     
    
    while (abs(turtle_theta) - abs(final_angle)) > 0.1:
        velocity_publisher.publish(vel)

    #original code for rotating the turtle using calculus
    #while (current_angle <= relative_angle):
    #   velocity_publisher.publish(vel)
    #   t1 = rospy.Time.now().to_sec()
    #   current_angle = ang_vel*(t1-t0)

    #Stop the turtle
    vel.angular.z = 0
    velocity_publisher.publish(vel)
    print("Relative Angle:")
    print(final_angle)
    print("Starting Angle:")
    print(starting_angle)


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
    while(abs(current_distance) < abs(distance)):
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
        rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
        rate = rospy.Rate(10) #10 hz
        draw_s()
    except rospy.ROSInterruptException: pass
