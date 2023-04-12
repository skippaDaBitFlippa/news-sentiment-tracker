import os
import sys
import time
import socket
from subprocess import call

def wait_for_service(host, port, retries=10, delay=5):
    for _ in range(retries):
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(delay)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 entrypoint.py <script_to_run>")
        sys.exit(1)

    script_to_run = sys.argv[1]

    kafka_host = os.environ.get("KAFKA_HOST", "kafka")
    kafka_port = int(os.environ.get("KAFKA_PORT", "9092"))

    if wait_for_service(kafka_host, kafka_port):
        call(["python3", script_to_run])
    else:
        print(f"Kafka service not available at {kafka_host}:{kafka_port}")
        sys.exit(1)
