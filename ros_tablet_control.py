import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class ROS2ToSerial(Node):
    def __init__(self):
        super().__init__('ros2_to_serial')

        # Set up serial communication with STM32
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        # Create a subscriber for the 'actuator_topic'
        self.subscription = self.create_subscription(
            String,
            'actuator_topic',  # Single topic for mode and pwm value
            self.actuator_pwm_callback,
            10
        )
        
        self.get_logger().info('Subscriber node initialized and listening to actuator_topic.')

    def actuator_pwm_callback(self, msg):
        # Received message is expected to be in the format "mode pwm_value"
        received_data = msg.data
        self.get_logger().info(f'Received data: {received_data}')

        # Send the received string directly to STM32 over serial
        self.send_to_stm32(received_data)

    def send_to_stm32(self, data):
        # Send data to the STM32 via the serial connection
        self.ser.write((data + '\n').encode('utf-8'))
        self.get_logger().info(f'Sent to STM32: {data}')

    def __del__(self):
        # Close the serial port when done
        self.ser.close()

def main(args=None):
    # Initialize the ROS2 Python client library
    rclpy.init(args=args)

    # Create the ROS2 node
    node = ROS2ToSerial()

    # Spin the node so it keeps running
    rclpy.spin(node)

    # Shutdown when done
    rclpy.shutdown()

if __name__ == '__main__':
    main()
