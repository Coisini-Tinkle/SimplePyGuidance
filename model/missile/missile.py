# -*- encoding: utf-8 -*-
import numpy as np
from utils.visualize import visualize
from model.object.object import Object

'''
@File    :   missile.py
@Time    :   2024/10/17 14:41:55
@Author  :   Yao Zhang 
@Version :   3.6
@Github  :  https://github.com/Coisini-Tinkle
'''


class missile():
    def __init__(self, v, theta) -> None:
        '''

        :param v: The original velocity of missile
        :param theta: The angle between the target speed and the horizontal line, in degrees
        '''
        self.v = v
        self.theta = theta

        self.time_list = list()
        self.x_list = list()
        self.y_list = list()
        self.v_list = list()
        self.theta_list = list()


# In this project, we assume that the missile's speed is constant for convenience. In addition, in order to catch up with the target, the missile's speed should be set larger.
def TrackingModel(missile: missile, target: Object, time_end: int, delta_time: float, eps=10e-2):
    '''

    :param missile:
    :param target:
    :param time_end:
    :param delta_time:
    :return:
    '''

    index = np.uint(time_end / delta_time)
    t_theta = target.theta * np.pi / 180  # this value stays same

    r_list = list()
    q_list = list()

    # init
    missile.x_list.append(0)
    missile.y_list.append(0)
    missile.time_list.append(0)
    missile.v_list.append(missile.v)
    missile.theta_list.append(missile.theta * np.pi / 180)
    r_list.append(target.height_0)
    q_list.append(np.pi / 2)

    for i in range(index):
        t_x = target.x_list[i]
        t_y = target.y_list[i]
        t_v = target.v_list[i]
        m_x = missile.x_list[i]
        m_y = missile.y_list[i]

        if np.abs(r_list[i]) < eps:
            print("Successfully!")
            break

        dr_dt = t_v * np.cos(q_list[i] - t_theta) - missile.v_list[i]
        r_dq_dt = -t_v * np.sin(q_list[i] - t_theta)
        dq_dt = r_dq_dt / r_list[i]

        r_list.append(r_list[i] + dr_dt * delta_time)
        q_list.append(q_list[i] + dq_dt * delta_time)
        missile.theta_list.append(q_list[i] + dq_dt * delta_time)
        missile.x_list.append(missile.x_list[i] + missile.v_list[i] * delta_time * np.cos(missile.theta_list[i]))
        missile.y_list.append(missile.y_list[i] + missile.v_list[i] * delta_time * np.sin(missile.theta_list[i]))
        missile.v_list.append(missile.v)
        missile.time_list.append(i * delta_time)

    missile.q_list = q_list
    missile.r_list = r_list


def ParallelModel(missile: missile, target: Object, time_end: int, delta_time: float, eps=10e-2):
    index = np.uint(time_end / delta_time)
    t_theta = target.theta * np.pi / 180  # this value stays same

    r_list = list()
    q_list = list()

    # init
    missile.x_list.append(0)
    missile.y_list.append(0)
    missile.time_list.append(0)
    missile.v_list.append(missile.v)
    missile.theta_list.append(missile.theta * np.pi / 180)
    r_list.append(target.height_0)
    q_list.append(np.pi / 2)

    for i in range(index):
        t_x = target.x_list[i]
        t_y = target.y_list[i]
        t_v = target.v_list[i]
        m_x = missile.x_list[i]
        m_y = missile.y_list[i]

        if np.abs(r_list[i]) < eps:
            print("Successfully!")
            break

        dr_dt = t_v * np.cos(q_list[i] - t_theta) - missile.v_list[i] * np.cos(q_list[i] - missile.theta_list[i])
        # r_dq_dt = -t_v * np.sin(q_list[i] - t_theta) + missile.v_list[i] * np.sin(q_list[i] - missile.theta_list[i])
        # dq_dt = r_dq_dt / r_list[i]
        dq_dt = 0
        temp1 = t_v * np.sin(q_list[i] - t_theta) / missile.v_list[i]  # np.sin(q_list[i] - missile.theta_list[i])
        temp2 = np.arcsin(temp1)  # np.sin(q_list[i] - missile.theta_list[i])
        # 注意一下反三角函数的取值

        r_list.append(r_list[i] + dr_dt * delta_time)
        q_list.append(q_list[i] + dq_dt * delta_time)
        missile.theta_list.append(q_list[i] - temp2)
        missile.x_list.append(missile.x_list[i] + missile.v_list[i] * delta_time * np.cos(missile.theta_list[i]))
        missile.y_list.append(missile.y_list[i] + missile.v_list[i] * delta_time * np.sin(missile.theta_list[i]))
        missile.v_list.append(missile.v)
        missile.time_list.append(i * delta_time)

    missile.q_list = q_list
    missile.r_list = r_list


def RatioModel(missile: missile, target: Object, time_end: int, delta_time: float, k: int, eps=10e-2):
    index = np.uint(time_end / delta_time)
    t_theta = target.theta * np.pi / 180  # this value stays same

    r_list = list()
    q_list = list()

    # init
    missile.x_list.append(0)
    missile.y_list.append(0)
    missile.time_list.append(0)
    missile.v_list.append(missile.v)
    missile.theta_list.append(missile.theta * np.pi / 180)
    r_list.append(target.height_0)
    q_list.append(np.pi / 2)

    for i in range(index):
        t_x = target.x_list[i]
        t_y = target.y_list[i]
        t_v = target.v_list[i]
        m_x = missile.x_list[i]
        m_y = missile.y_list[i]

        if np.abs(r_list[i]) < eps:
            print("Successfully!")
            break

        dr_dt = t_v * np.cos(q_list[i] - t_theta) - missile.v_list[i] * np.cos(q_list[i] - missile.theta_list[i])
        r_dq_dt = -t_v * np.sin(q_list[i] - t_theta) + missile.v_list[i] * np.sin(q_list[i] - missile.theta_list[i])
        dq_dt = r_dq_dt / r_list[i]
        dtheta_dt = k * dq_dt

        r_list.append(r_list[i] + dr_dt * delta_time)
        q_list.append(q_list[i] + dq_dt * delta_time)
        missile.theta_list.append(missile.theta_list[i] + dtheta_dt * delta_time)
        missile.x_list.append(missile.x_list[i] + missile.v_list[i] * delta_time * np.cos(missile.theta_list[i]))
        missile.y_list.append(missile.y_list[i] + missile.v_list[i] * delta_time * np.sin(missile.theta_list[i]))

        missile.v_list.append(missile.v)
        missile.time_list.append(i * delta_time)

    missile.q_list = q_list
    missile.r_list = r_list


def ImprovedRatioModel(missile: missile, target: Object, time_end: int, delta_time: float, k_base: int, eps=10e-2,
                       adaptive_k=False):
    index = np.uint(time_end / delta_time)
    t_theta = target.theta * np.pi / 180  # 目标初始角度保持不变

    r_list = list()
    q_list = list()

    # 初始化导弹的属性列表
    missile.x_list.append(0)
    missile.y_list.append(0)
    missile.time_list.append(0)
    missile.v_list.append(missile.v)
    missile.theta_list.append(missile.theta * np.pi / 180)
    r_list.append(target.height_0)
    q_list.append(np.pi / 2)

    for i in range(index):
        t_x = target.x_list[i]
        t_y = target.y_list[i]
        t_v = target.v_list[i]
        m_x = missile.x_list[i]
        m_y = missile.y_list[i]

        if np.abs(r_list[i]) < eps:
            print("Hit target successfully!")
            break

        # 计算目标与导弹的相对距离与速度
        dr_dt = t_v * np.cos(q_list[i] - t_theta) - missile.v_list[i] * np.cos(q_list[i] - missile.theta_list[i])
        r_dq_dt = -t_v * np.sin(q_list[i] - t_theta) + missile.v_list[i] * np.sin(q_list[i] - missile.theta_list[i])
        dq_dt = r_dq_dt / r_list[i]

        # 如果启用自适应比例因子，根据距离自适应调整k值
        if adaptive_k:
            k = k_base * (1 + 0.5 * np.exp(-0.1 * r_list[i]))  # 自适应k
        else:
            k = k_base

        dtheta_dt = k * dq_dt

        # 更新距离、角度和导弹的位置信息
        r_list.append(r_list[i] + dr_dt * delta_time)
        q_list.append(q_list[i] + dq_dt * delta_time)
        missile.theta_list.append(missile.theta_list[i] + dtheta_dt * delta_time)
        missile.x_list.append(missile.x_list[i] + missile.v_list[i] * delta_time * np.cos(missile.theta_list[i]))
        missile.y_list.append(missile.y_list[i] + missile.v_list[i] * delta_time * np.sin(missile.theta_list[i]))

        missile.v_list.append(missile.v)
        missile.time_list.append(i * delta_time)

    missile.q_list = q_list
    missile.r_list = r_list


def RatioModelWithImpactAngleConstraint(missile: missile, target: Object, time_end: int, delta_time: float, k: int,
                                        desired_impact_angle=60, eps=10e-2):
    index = int(time_end / delta_time)
    t_theta = target.theta * np.pi / 180  # 目标初始角度
    impact_angle_rad = desired_impact_angle * np.pi / 180  # 落角约束（转换为弧度）

    r_list = list()
    q_list = list()

    # 初始化导弹的属性列表
    missile.x_list.append(0)
    missile.y_list.append(0)
    missile.time_list.append(0)
    missile.v_list.append(missile.v)
    missile.theta_list.append(missile.theta * np.pi / 180)
    r_list.append(target.height_0)
    q_list.append(np.pi / 2)

    for i in range(index):
        t_x = target.x_list[i]
        t_y = target.y_list[i]
        t_v = target.v_list[i]
        m_x = missile.x_list[i]
        m_y = missile.y_list[i]

        if np.abs(r_list[i]) < eps:
            print("Hit target successfully with impact angle constraint!")
            break

        # 计算目标与导弹的相对距离与速度
        dr_dt = t_v * np.cos(q_list[i] - t_theta) - missile.v_list[i] * np.cos(q_list[i] - missile.theta_list[i])
        r_dq_dt = -t_v * np.sin(q_list[i] - t_theta) + missile.v_list[i] * np.sin(q_list[i] - missile.theta_list[i])
        dq_dt = r_dq_dt / r_list[i]

        # 计算落角误差，并应用到导引律中
        impact_angle_error = impact_angle_rad - missile.theta_list[i]
        dtheta_dt = k * dq_dt + 0.5 * impact_angle_error  # 增加落角误差控制项

        # 更新距离、角度和导弹的位置信息
        r_list.append(r_list[i] + dr_dt * delta_time)
        q_list.append(q_list[i] + dq_dt * delta_time)
        missile.theta_list.append(missile.theta_list[i] + dtheta_dt * delta_time)
        missile.x_list.append(missile.x_list[i] + missile.v_list[i] * delta_time * np.cos(missile.theta_list[i]))
        missile.y_list.append(missile.y_list[i] + missile.v_list[i] * delta_time * np.sin(missile.theta_list[i]))

        missile.v_list.append(missile.v)
        missile.time_list.append(i * delta_time)

    missile.q_list = q_list
    missile.r_list = r_list


if __name__ == '__main__':
    target = Object(10, 1, 30, 40)
    missile = missile(25, 69.5)
    target.generate_trajectory(time_end=1000, delta_time=0.01)
    # TrackingModel(missile, target, time_end=1000, delta_time=0.01)
    ParallelModel(missile, target, time_end=1000, delta_time=0.01)
    # RatioModel(missile, target, time_end=1000, delta_time=0.01, k=5)
    visualize.visualize_missile(missile)
