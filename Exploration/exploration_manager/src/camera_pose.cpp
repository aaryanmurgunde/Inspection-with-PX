#include <ros/ros.h>
#include <math.h>
#include <geometry_msgs/PoseStamped.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
ros::Publisher pub_pose;

float degreeToRad(float degree){
    float pi = 3.1415;
    return (degree * (pi/180));
}

void cameraPoseCallback(const geometry_msgs::PoseStamped::ConstPtr& data){
    geometry_msgs::PoseStamped camera_pose;
    camera_pose = *data;
    tf2::Quaternion q_orig, q_rot, q_new;
    //Quaternion conversion
    tf2::convert(camera_pose.pose.orientation , q_orig);
    q_rot.setRPY(degreeToRad(90.0) , 0, degreeToRad(-90.0));
    q_new = q_rot*q_orig;
    q_new.normalize();
    tf2::convert(q_new, camera_pose.pose.orientation);
    pub_pose.publish(camera_pose);
}

int main(int argc, char** argv) {
  ros::init(argc, argv, "camera_pose");
  ros::NodeHandle nh;
  ros::Subscriber mavros_sub;

  mavros_sub = nh.subscribe<geometry_msgs::PoseStamped>( "/mavros/local_position/pose", 1000,  cameraPoseCallback);  


  pub_pose  = nh.advertise<geometry_msgs::PoseStamped>("/camera_pose",1000);

  ros::AsyncSpinner spinner(1);
  spinner.start();
    ros::waitForShutdown();
  return 0;
}
