import re
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import TwistStamped

LINEAR_SPEED = 0.10    # meters per second
ANGULAR_SPEED = 0.50   # radians per second
MOVE_TIME = 1.0        # seconds


class VoiceController(Node):
    def __init__(self):
        super().__init__("voice_controller")

        self.subscription = self.create_subscription(
            String, "transcription", self.on_text, 10
        )
        self.publisher = self.create_publisher(TwistStamped, "cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.on_timer)

        self.linear = 0.0
        self.angular = 0.0
        self.stop_time = 0.0

        self.get_logger().info("Voice controller is ready.")

    def now_seconds(self):
        return self.get_clock().now().nanoseconds / 1e9

    def on_text(self, msg):
        text = re.sub(r"[^a-z ]", "", msg.data.lower())
        words = text.split()
        self.get_logger().info(f"Received: {text}")

        if "stop" in words:
            self.linear = 0.0
            self.angular = 0.0
        elif "forward" in words:
            self.linear = LINEAR_SPEED
            self.angular = 0.0
        elif "back" in words or "backward" in words:
            self.linear = -LINEAR_SPEED
            self.angular = 0.0
        elif "left" in words:
            self.linear = 0.0
            self.angular = ANGULAR_SPEED
        elif "right" in words:
            self.linear = 0.0
            self.angular = -ANGULAR_SPEED
        else:
            self.get_logger().info("No command found.")
            return

        self.stop_time = self.now_seconds() + MOVE_TIME

    def on_timer(self):
        if self.now_seconds() < self.stop_time:
            self.send_speed(self.linear, self.angular)
        else:
            self.send_speed(0.0, 0.0)

    def send_speed(self, linear, angular):
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.twist.linear.x = linear
        cmd.twist.angular.z = angular
        self.publisher.publish(cmd)


def main():
    rclpy.init()
    node = VoiceController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.send_speed(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
