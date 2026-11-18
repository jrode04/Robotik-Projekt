import sys
import time
import rclpy
from std_msgs.msg import String
import whisper

audio_file = sys.argv[1]

# Step 1: Transcribe the audio
model = whisper.load_model("base", device="cpu")
result = model.transcribe(audio_file, fp16=False)
text = result["text"].strip()

with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("Text saved:", text)

# Step 2: Send the text to the robot
rclpy.init()
node = rclpy.create_node("transcription_publisher")
publisher = node.create_publisher(String, "transcription", 10)

# Wait up to 10 seconds for a listener
start = time.time()
while publisher.get_subscription_count() == 0 and time.time() - start < 10:
    rclpy.spin_once(node, timeout_sec=0.5)

msg = String()
msg.data = text
publisher.publish(msg)
print("Message sent to topic /transcription")

time.sleep(1)
node.destroy_node()
rclpy.shutdown()