# ../usr/bin/envclass missile():
# -*- encoding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt

'''
@File    :   object.py
@Time    :   2024/10/17 14:17:53
@Author  :   Yao Zhang 
@Version :   3.6
@Github  :  https://github.com/Coisini-Tinkle
'''


class Object():
    def __init__(self, v, a, theta, height_0, v_a_theta=0) -> None:
        """the initialize of object instance

        Args:
            v (_float_): The original velocity of object(or target)
            a (_float_): The acceleration of the target, whose value is always a constant
            theta (_float_): The angle between the target speed and the horizontal line, in degrees
            height_0 (_float_): The original height of target above horizon
        """
        self.v = v
        self.a = a
        self.theta = theta
        self.height_0 = height_0
        self.v_a_theta = v_a_theta

    def generate_trajectory(self, time_end: int, delta_time: float) -> np.array:
        """The trajectory of the target is calculated by iteration.

        The target moves in a straight line with uniform acceleration

        Args:
            time_end (_int_): Simulation end time. ATTENTION:this value stays same between missile and target.
            delta_time (_float_): Simulation minimum step size. ATTENTION:this value stays same between missile and target.
        """
        self.time_list = list()
        self.x_list = list()
        self.y_list = list()
        self.v_list = list()

        # the initial velocity
        vx0 = self.v * math.cos(math.radians(self.theta))
        vy0 = self.v * math.sin(math.radians(self.theta))
        ax = self.a * math.cos(math.radians(self.theta + self.v_a_theta))
        ay = self.a * math.sin(math.radians(self.theta + self.v_a_theta))

        index = np.uint(time_end / delta_time)
        for i in range(index):
            t = i * delta_time
            self.time_list.append(t)
            vx = vx0 + ax * t
            vy = vy0 + ay * t
            self.v_list.append(math.sqrt(vx**2 + vy**2))
            self.x_list.append(vx0 * t + ax * t * t / 2)
            self.y_list.append(self.height_0 + vy0 * t +ay * t * t / 2)


if __name__ == '__main__':
    target = Object(10, 5, 30, 40,30)
    target.generate_trajectory(time_end=50, delta_time=0.1)

    fig = plt.figure(figsize=(12, 8))

    plt.subplot(221)
    plt.plot(target.time_list, target.x_list, label='x position', color='blue')
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('X Position vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(222)
    plt.plot(target.time_list, target.y_list, label='y position', color='green')
    plt.xlabel('Time')
    plt.ylabel('y')
    plt.title('Y Position vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(223)
    plt.plot(target.time_list, target.v_list, label='velocity', color='red')
    plt.xlabel('Time')
    plt.ylabel('v')
    plt.title('Velocity vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(224)
    plt.plot(target.x_list, target.y_list, label='Trajectory', color='purple')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Trajectory in XY Plane')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.tight_layout()
    plt.show()
