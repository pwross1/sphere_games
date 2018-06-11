import numpy as np
import rospy

from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Point

def find_spheros(image_data):
    image_array = np.fromstring(image_data.data, np.uint8)
    cv2_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    rospy.init_node('sphere_finder', anonymous=True)

    red_center = rospy.Publisher('/red_sphero/center', Point, queue_size=1)
    blue_center = rospy.Publisher('/blue_sphero/center', Point, queue_size=1)

    cap = cv2.VideoCapture(0)
    cap = 
    rate = rospy.Rate(10) # Hz
    while not rospy.is_shutdown():
        ret, frame = cap.read()

        # Mask by hue and find center
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_lower_1 = np.array([0, 50, 50])
        red_upper_1 = np.array([int(1.0 * 180. / 9.), 255, 255])
        red_mask_1 = cv2.inRange(hsv, red_lower_1, red_upper_1)

red_mask = red_mask_1 + red_mask_2
        red_mask = cv2.erode(red_mask, None, iterations=5)
        red_mask = cv2.dilate(red_mask, None, iterations=5)

        blue_lower = np.array([int(3.0 * 180. / 6.), 150, 150])
        blue_upper = np.array([int(4.5 * 180. / 6.), 200, 200])
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        blue_mask = cv2.erode(blue_mask, None, iterations=2)
        blue_mask = cv2.dilate(blue_mask, None, iterations=2)

        red_contours = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(red_contours) > 0:
            red_M = cv2.moments(max(red_contours, key=cv2.contourArea))
            red_center = Point(int(red_M['m10'] / red_M['m00']), int(red_M['m01'] / red_M['m00']), 0)
            print red_center
            sphero_center.publish(red_center)

        blue_contours = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(blue_contours) > 0:
            blue_M = cv2.moments(max(blue_contours, key=cv2.contourArea))
            blue_center = Point(int(blue_M['m10'] / blue_M['m00']), int(blue_M['m01'] / blue_M['m00']), 0)
            print blue_center
            sphero_center.publish(blue_center)

        cv2.imshow('frame', frame)
        cv2.imshow('red mask', red_mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return

def pub_sub_init():
    pub_red = rospy.Publisher('/red_sphero/center', Point, queue_size=1)
    pub_blue = rospy.Publisher('/blue_sphero/center', Point, queue_size=1)

    sub_image = rospy.Subscriber('/raspicam_node/image/compressed', CompressedImage, find_spheros, queue_size=1)

    rospy.init_node('camera_host', anonymous=True)

    rate = rospy.Rate(10) # Hz
    while not rospy.is_shutdown():
        rate.sleep()
    return

if __name__ == '__main__':
    try:
        pub_sub_init()
    except rospy.ROSInterruptException:
        pass
