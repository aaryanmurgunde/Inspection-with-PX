#!/usr/bin/env python

import rospy
from quadrotor_msgs.msg import PositionCommand # for Fast-Planner
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import PoseStamped

class MessageConverter:
    def __init__(self):
        rospy.init_node('trajectory_msg_converter')

        self.pose = PoseStamped()
        self.pose.pose.position.x = 0
        self.pose.pose.position.y = 0
        self.pose.pose.position.z = 1
        self.pose.pose.orientation.x = 0
        self.pose.pose.orientation.y = 0
        self.pose.pose.orientation.z = 0
        self.pose.pose.orientation.w = 1
        
        self.traj_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=1)
        rospy.Subscriber('planning/pos_cmd', PositionCommand, self.fastPlannerTrajCallback)
    

    def fastPlannerTrajCallback(self, msg):
        # position and yaw
        self.pose.pose.position.x = msg.position.x
        self.pose.pose.position.y = msg.position.y
        self.pose.pose.position.z = msg.position.z
        q = quaternion_from_euler(0, 0, msg.yaw) # RPY
        self.pose.pose.orientation.x = q[0]
        self.pose.pose.orientation.y = q[1]
        self.pose.pose.orientation.z = q[2]
        self.pose.pose.orientation.w = q[3]

    def run(self):
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            self.traj_pub.publish(self.pose)
            rate.sleep()

if __name__ == '__main__':
    obj = MessageConverter()
    obj.run()
