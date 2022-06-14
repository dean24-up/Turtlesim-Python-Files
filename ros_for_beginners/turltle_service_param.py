#!/usr/bin/env python3

#turtle_service_param.py
#sets background color parameter and resets workspace using /reset service

#Credit to ch 5 of https://github.com/Apress/Robot-Operating-System-Abs-Begs for code
#downloaded dean24-up 6/13/22
#see p. 233 pdf of https://link.springer.com/content/pdf/10.1007/978-1-4842-7750-8.pdf for tutorial

import rospy

import random

from std_srvs.srv import Empty  #empty is the type of serrvice corresponding to reset


def change_color():

    rospy.init_node('change_color', anonymous=False)
    rospy.set_param('/turtlesim/background_b',random.randint(0,255))
    rospy.set_param('/turtlesim/background_g',random.randint(0,255))
    rospy.set_param('/turtlesim/background_r',random.randint(0,255))

    rospy.wait_for_service('/reset')

    try:

        serv = rospy.ServiceProxy('/reset',Empty)
        resp = serv()
        rospy.loginfo("Executed service")

    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed: %s" %e)


    rospy.spin()

if __name__ == '__main__':
    try:
        change_color()
    except rospy.ROSInterruptException:
        pass
