#!/usr/bin/env python3

#https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
import numpy as np
import cv2

import rospy
import cv_bridge
from sensor_msgs.msg import Image

class ImageNode():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.K = None
        self.D = None
        self.R = None
        self.P = None


    def initialize(self, ns="~"):
        # Get params
        self.width = rospy.get_param(ns + "image_width")
        self.height = rospy.get_param(ns + "image_height")
        self.K = rospy.get_param(ns + "camera_matrix/data")
        self.D = rospy.get_param(ns + "distortion_coefficients/data")
        self.R = rospy.get_param(ns + "rectification_matrix/data")
        self.P = rospy.get_param(ns + "projection_matrix/data")
        # reshape information
        self.K = np.array(self.K).reshape((3, 3))
        self.D = np.array(self.D)
        # Get topics
        self.sub_topic = rospy.get_param(ns + "sub_topic")
        self.pub_topic = rospy.get_param(ns + "pub_topic")
        # Get publishers
        self.sub_image = rospy.Subscriber(self.sub_topic, Image, self.image_callback, None, 10)
        self.pub_image = rospy.Publisher(self.pub_topic, Image, queue_size = 10)

        self.bridge = cv_bridge.CvBridge()


    def image_callback(self, msg):
        #decode the compressed image
        img = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        h,  w = img.shape[:2]
        new_K, roi = cv2.getOptimalNewCameraMatrix(self.K, self.D, (w,h), 1, (w,h))
        # undistort
        mapx, mapy = cv2.initUndistortRectifyMap(self.K, self.D, None, new_K, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        # crop the image
        x, y, w, h = roi
        #dst = dst[y:y+h, x:x+w]

        img_msg = self.bridge.cv2_to_imgmsg(dst, encoding="bgr8")
        img_msg.header.stamp = rospy.Time.now()
        self.pub_image.publish(img_msg)
        

if __name__ == '__main__':

    #init the node
    rospy.init_node("rectification_node", log_level=rospy.INFO)

    rospy.loginfo("Start rectifying images...")

    node = ImageNode()
    node.initialize()

    rospy.spin()
