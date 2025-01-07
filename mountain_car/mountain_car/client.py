import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class DQNClient(Node):
    def __init__(self):
        super().__init__('car_dqn_client')
        self.client = self.create_client(Trigger, 'start_simulation')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for the server...")

        self.send_request()

    def send_request(self):
        request = Trigger.Request()
        self.future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, self.future)

        if self.future.result() is not None:
            self.get_logger().info(f"Result: {self.future.result().message}")
        else:
            self.get_logger().error("Service call failed")


def main(args=None):
    rclpy.init(args=args)
    node = DQNClient()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
