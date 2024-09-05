#! /usr/bin/env python3

# Base functions
import rclpy
from rclpy.node import Node
from cv2 import destroyAllWindows

# Import messages
from diegetic_button_pkg.msg import InputStatusArray
from sensor_msgs.msg import Joy
# import socket

from collections import deque

import datetime


    

    
class ControllerPublisher(Node):

    def __init__(self):

        super().__init__("IoT_node")

        # Subscribers
        self.subscriber_input_listener = self.create_subscription(
            InputStatusArray, "diegetic/inputs", self.update_controller, 1
        )


        # Dictionary for mapping inputs to axes
        self.button = {
            "TL": 1,
            "TR": 2,
        }

        self.get_logger().info("Ready to publish joystick messages.")
        
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect(('127.0.0.1', 65111))
        # self.get_logger().info(f"Connected to server '127.0.0.1':65111")
        self.filename='homeassistant/log.json'
        self.buttoninput = deque(maxlen=100)
        self.true_count=0
        self.state=0 # 0=off 1=on

    def update_controller(self, InputStatusArray_msg):

        # Unpack InputStatusArray_msg
        inputs = InputStatusArray_msg.inputs

        joy_msg = Joy()
        joy_msg.header.stamp = self.get_clock().now().to_msg()
        joy_msg.header.frame_id = "joy"

        joy_msg.buttons = [0] * 3

        for input in inputs:

            # Buttons
            if input.input_id in self.button:
                # Only do if status == active
                if input.status == "active":
                    joy_msg.buttons[self.button[input.input_id]] = int(input.percent)
                else:
                    joy_msg.buttons[self.button[input.input_id]] = 0

        # joy_msg.header.stamp = InputStatusArray_msg.header.stamp
        # self.get_logger().info(str(joy_msg.buttons))
        # self.client_socket.sendall(message.encode())
        # self.get_logger().info(f"Sent: {message}")
        self.true_count += joy_msg.buttons[2]
        self.buttoninput.append(joy_msg.buttons[2])
        
        if len(self.buttoninput) > 100:
            oldest_value = self.buttoninput.popleft()
            self.true_count -= oldest_value

        if self.true_count >= 60:
            if self.state==0:
                self.state=1
            elif self.state==1:
                self.state=0
            try:
                with open(self.filename, 'w') as file:
                    file.write(str(self.state))
                self.get_logger().info(f"Message {str(self.state)} successfully written to {self.filename}")
            except Exception as e:
                self.get_logger().info(f"An error occurred: {e}")
            self.buttoninput = deque(maxlen=100)
            self.true_count = 0
            current_time = datetime.datetime.now()
            self.get_logger().info(str(current_time))

        
        


def main():
    rclpy.init()  # Initialize ROS DDS
    controller_publisher = ControllerPublisher()  # Create instance of function

    print("Glasses Joy Publisher Node is Running...")

    try:
        rclpy.spin(controller_publisher)  # prevents closure. Run until interrupt
        
    except KeyboardInterrupt:
        controller_publisher.client_socket.close()
        destroyAllWindows()
        controller_publisher.destroy_node()  # duh
        rclpy.shutdown()  # Shutdown DDS !


if __name__ == "__main__":
    main()
    


"""
header:
stamp:
    sec: 1665419855
    nanosec: 220658939
frame_id: joy
axes:
- -0.0  L X (Left pos)
- -0.007923568598926067 L Y
- 1.0 L Trigger
- -0.020677093416452408 R X
- -0.037381961941719055 R Y
- 1.0 R T
- 0.0 Dpad X
- 0.0 Dpad Y
buttons:
- 0 A
- 0 B
- 0 X
- 0 Y
- 0 LB
- 0 RB
- 0 Select
- 0 Start
- 0 Xbox
- 0 LP
- 0 RP
---

"""
