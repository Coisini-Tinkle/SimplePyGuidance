# ../usr/bin/env pytorch.python
# -*- encoding: utf-8 -*-

'''
@File    :   main.py
@Time    :   2024/10/17 15:22:33
@Author  :   Yao Zhang 
@Version :   3.6
@Github  :  https://github.com/Coisini-Tinkle
'''
import argparse

import numpy as np
import yaml
import time
import os
import model
import csv
from utils import *


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('cfg', type=str, default='', help='config.yaml path')
    default_output_dir = str(os.getcwd()) + '/output/'
    parser.add_argument("-out_dir", type=str, help="the output folder,please end with '/'", default=default_output_dir)

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt


def main(opt):
    with open(opt.cfg, 'r') as file:
        cfg = yaml.safe_load(file)

    t_v = cfg['t_v']
    t_a = cfg['t_a']
    t_theta = cfg['t_theta']
    t_height_0 = cfg['t_height_0']

    time_end = cfg['time_end']
    delta_time = cfg['delta_time']
    eps = np.float(cfg['eps'])

    m_v = cfg['m_v']
    m_theta = cfg['m_theta']

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(opt.out_dir, timestamp)

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory: {e}")
        return

    # Copy the config file to the output directory
    try:
        with open(opt.cfg, 'r') as file:
            config_content = file.read()
        with open(os.path.join(output_dir, 'config.yaml'), 'w') as file:
            file.write(config_content)
    except Exception as e:
        print(f"Error copying config file: {e}")
        return

    target = model.Object(t_v, t_a, t_theta, t_height_0)
    target.generate_trajectory(time_end, delta_time)
    missile = model.missile(m_v, m_theta)
    guidance_methods = {
        "TrackingModel": model.TrackingModel,
        "ParallelModel": model.ParallelModel,
        "RatioModel": model.RatioModel,
        "ImprovedRatioModel":model.ImprovedRatioModel,
        "RatioModelWithImpactAngleConstraint":model.RatioModelWithImpactAngleConstraint,
    }
    guidance_method = cfg.get('guidance_method')
    k = cfg.get('k')

    if guidance_method in guidance_methods:
        if guidance_method in ["RatioModel","ImprovedRatioModel","RatioModelWithImpactAngleConstraint"]:
            guidance_methods[guidance_method](missile, target, time_end, delta_time, k, eps)
        else:
            guidance_methods[guidance_method](missile, target, time_end, delta_time, eps)
    else:
        print(f"Unknown guidance method: {guidance_method}")

    file_path = os.path.join(output_dir, 'trajectory_data.csv')
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Time', 'X', 'Y', 'Velocity', 'Theta', 'r', 'q'])

            # 写入 target 数据
            for t, x, y, v in zip(target.time_list, target.x_list, target.y_list, target.v_list):
                writer.writerow(['Target', t, x, y, v, None, None, None])  # None for theta, as it's not from target

            # 写入 missile 数据
            for t, r, q, x, y, v, theta in zip(missile.time_list, missile.r_list, missile.q_list, missile.x_list,
                                               missile.y_list, missile.v_list, missile.theta_list):
                writer.writerow(['Missile', t, x, y, v, theta, r, q])

        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
    target_plot_path = os.path.join(output_dir, "target_trajectory.png")
    missile_plot_path = os.path.join(output_dir, "missile_trajectory.png")
    plot_path = os.path.join(output_dir, "2_trajectory.png")
    visualize_object(target, show=False, save=target_plot_path)
    visualize_missile(missile, show=False, save=missile_plot_path)
    visualize2(target, missile, show=False, save=plot_path)


if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
