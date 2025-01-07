import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import os
import gymnasium as gym
import numpy as np
import bpu_infer_lib


class DQNServer(Node):
    def __init__(self):
        super().__init__('car_dqn_server')
        self.declare_parameter('model_path', '/root/car_dqn_output.bin')
        self.srv = self.create_service(Trigger, 'start_simulation', self.start_simulation_callback)
        self.get_logger().info("DQN Server is ready.")

    def start_simulation_callback(self, request, response):
        model_path = self.get_parameter('model_path').value
        self.get_logger().info(f"Using model path: {model_path}")
        
        # Initialize the environment and policy network
        epi_r = 0
        env = gym.make('MountainCar-v0', render_mode="human")
        s, _ = env.reset()
        step = 0
        policy_net = bpu_infer_lib.Infer(False)
        policy_net.load_model(model_path)

        while True:
            step += 1
            policy_net.read_input(s, 0)
            policy_net.forward(more=True)
            policy_net.get_output()
            action = np.argmax(policy_net.outputs[0].data.reshape(3))
            sp, r, done, truncate, _ = env.step(action.squeeze().item())
            epi_r += r
            s = sp
            if done:
                env.reset()
                break

        self.get_logger().info(f"Episode reward: {epi_r}, Steps: {step}")
        response.success = True
        response.message = f"Simulation completed: epi_r = {epi_r}, steps = {step}"
        return response


def main(args=None):
    rclpy.init(args=args)
    node = DQNServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()