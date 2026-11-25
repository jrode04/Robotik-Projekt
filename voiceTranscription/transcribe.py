import queue
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from listener import Listener


class TranscriptionPublisher(Node):
    def __init__(self):
        super().__init__("transcription_publisher")

        self.publisher = self.create_publisher(String, "transcription", 10)
        self.timer = self.create_timer(0.1, self.on_timer)
        self.done = False

        self.listener = Listener()
        self.listener.start()
        self.get_logger().info("Listening. Say 'finish' to stop.")

    def on_timer(self):
        try:
            text = self.listener.text_queue.get_nowait()
        except queue.Empty:
            if not self.listener.running:
                self.done = True
            return

        if self.publisher.get_subscription_count() == 0:
            self.get_logger().warning("No subscriber found.")

        msg = String()
        msg.data = text
        self.publisher.publish(msg)
        self.get_logger().info(f"Sent: {text}")


def main():
    rclpy.init()
    node = TranscriptionPublisher()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        node.listener.stop()
        time.sleep(1)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()