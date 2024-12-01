# ../usr/bin/env pytorch.python
# -*- encoding: utf-8 -*-
from model.object import object
from model.missile import missile
import matplotlib.pyplot as plt

'''
@File    :   visualize.py
@Time    :   2024/10/17 14:57:02
@Author  :   Yao Zhang 
@Version :   3.6
@Github  :  https://github.com/Coisini-Tinkle
'''


def visualize_object(target: object, show=True, save=None):
    '''
    the object instance has only three lists,as follows:
      time_list
      x_list
      y_list
      v_list
    the meanings of three lists are sane as lists in missile instance
    :param object: target object
    :param show: show or not
    :param save: the path to save plot
    :return:
    '''
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
    if show == True:
        plt.show()
    if save:
        plt.savefig(save)


def visualize_missile(missile: missile, show=True, save=None):
    '''
    missile instance has some lists , in order to have a good understanding of them, we summarize them as follows:
      time_list:time
      x_list:the x coordinate of missile
      y_list:the y coordinate of missile
      v_list:the velocity of missile, in our hypothesis, this value should stay same
      theta_list:the angle between missile's velocity and horizon ,in radians
      r_list:the list of modulus of the vector r
      q_list:the angle between vector r and horizon ,in radians
    :param missile: missile
    :param show: show or not
    :param save: the path to save plot
    :return:
    '''
    fig = plt.figure(figsize=(12, 16))

    plt.subplot(421)
    plt.plot(missile.time_list, missile.x_list, label='x position', color='blue')
    plt.xlabel('Time')
    plt.ylabel('x')
    plt.title('X Position vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(422)
    plt.plot(missile.time_list, missile.y_list, label='y position', color='green')
    plt.xlabel('Time')
    plt.ylabel('y')
    plt.title('Y Position vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(423)
    plt.plot(missile.time_list, missile.v_list, label='velocity', color='red')
    plt.xlabel('Time')
    plt.ylabel('v')
    plt.title('Velocity vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(424)
    plt.plot(missile.x_list, missile.y_list, label='Trajectory', color='purple')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Trajectory in XY Plane')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(425)
    plt.plot(missile.time_list, missile.theta_list, label='theta', color='m')
    plt.xlabel('Time')
    plt.ylabel('theta')
    plt.title('Theta vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(426)
    plt.plot(missile.time_list, missile.r_list, label='vector r', color='y')
    plt.xlabel('Time')
    plt.ylabel('r')
    plt.title('Vector r vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.subplot(427)
    plt.plot(missile.time_list, missile.q_list, label='angle_q', color='k')
    plt.xlabel('Time')
    plt.ylabel('q')
    plt.title('q vs Time')
    plt.grid(linestyle=":", color="r")
    plt.legend()

    plt.tight_layout()
    if show == True:
        plt.show()
    if save:
        plt.savefig(save)


# def visualize2(target: object, missile: missile, show=True, save=None):
#     t_list=missile.time_list
#     t_x_list=target.x_list[0:len(t_list)-1]
#     t_y_list=target.y_list[0:len(t_list)-1]
#     m_x_list=missile.x_list
#     m_y_list=missile.y_list
#
#     plt.figure(figsize=(10, 6))
#     plt.plot(t_x_list, t_y_list, label='Target Trajectory', color='blue')
#     plt.plot(m_x_list, m_y_list, label='Missile Trajectory', color='red')
#     plt.xlabel('X Position')
#     plt.ylabel('Y Position')
#     plt.title('Target and Missile Trajectories')
#     plt.legend()
#
#     if save is not None:
#         plt.savefig(save)
#     if show:
#         plt.show()

def visualize2(target: object, missile: object, show=True, save=None):
    t_list = missile.time_list
    t_x_list = target.x_list[0:len(t_list) - 1]
    t_y_list = target.y_list[0:len(t_list) - 1]
    m_x_list = missile.x_list
    m_y_list = missile.y_list

    plt.figure(figsize=(12, 8), facecolor='whitesmoke')
    plt.plot(t_x_list, t_y_list, label='Target Trajectory', color='blue', linewidth=2)
    plt.plot(m_x_list, m_y_list, label='Missile Trajectory', color='red', linewidth=2, linestyle='--')

    plt.xlabel('X Position', fontsize=14)
    plt.ylabel('Y Position', fontsize=14)
    plt.title('Target and Missile Trajectories', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(min(min(t_x_list), min(m_x_list)) - 1, max(max(t_x_list), max(m_x_list)) + 1)
    plt.ylim(min(min(t_y_list), min(m_y_list)) - 1, max(max(t_y_list), max(m_y_list)) + 1)
    plt.gca().set_facecolor('lightgrey')

    if save is not None:
        plt.savefig(save, bbox_inches='tight')
    if show:
        plt.show()