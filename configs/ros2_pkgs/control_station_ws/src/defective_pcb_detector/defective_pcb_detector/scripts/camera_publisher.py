#!/usr/bin/env python3
import sys
import os
sys.path.append('...')
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

from std_msgs.msg import Bool,String,Int16
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge


# from robot_custom_msgs.msg import gui_msg
import cv2


from defective_pcb_detector.realsense_class import RealSense_Cam, get_realsense_devices



# script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(script_dir)
# parent_parent_dir = os.path.dirname(parent_dir)




def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def image_resize(img, scale):
    image = Image.fromarray(img)
    new_width, new_height = int(image.width * scale), int(image.height * scale)
    img_res = image.resize((new_width, new_height), Image.LANCZOS)
    return img_res


class GUIROS(Node):
    def __init__(self):
        super().__init__("hand_landmark_monitoring")

        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz timer
       
        self.rawimages_publisher = self.create_publisher(Image , "rawframe_topcamera",10)

        self.imagebridge = CvBridge() # for conversion of cv images to ros2 images
        self.rawframe = None
        self.raw_imagebridge = CvBridge() 

    def timer_callback(self):
        depth, frame = cam.get_frame_from_realsense(pipeline,aligned_frame=False)
        if frame is None:
            self.get_logger().error("Failed to capture frame from RealSense!")
            return
        else:    

            self.rawframe = frame
            rawImage_tobesent = self.raw_imagebridge.cv2_to_imgmsg( self.rawframe, encoding='bgr8')
            self.rawimages_publisher.publish(rawImage_tobesent)

          
            
            
            # cv2.imshow('Align Example', final_image)
            # key = cv2.waitKey(1)
            # if key & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     rclpy.shutdown()
            #     exit()
        





list_of_devices = get_realsense_devices()
for index, device in  enumerate(list_of_devices):
    
    cam = RealSense_Cam(device["serial_number"])
    pipeline, config = cam.start_real_sense()
    # Start streaming
    pipeline.start(config)


# Start streaming
depth_scale, depth_intrin = cam.depth_information(pipeline)

def main():
    
    rclpy.init(args=None)
    node = GUIROS()
    rclpy.spin(node)
   
    pipeline.stop()

if __name__=="__main__":

    main()