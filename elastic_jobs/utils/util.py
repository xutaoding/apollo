# -*- coding: utf-8 -*-

import os
import os.path

TASK_PKG_NAME = 'tasks_pkg'
BASE_PATH = os.path.dirname(os.path.dirname(__file__))


def get_tasks_packages():
    packages = []
    base_path = BASE_PATH
    tasks_packages_name = TASK_PKG_NAME

    base_name = os.path.basename(base_path)
    packages_path = os.path.join(base_path, tasks_packages_name)

    for name in os.listdir(packages_path):
        fs_path = os.path.join(packages_path, name)

        if os.path.isdir(fs_path):
            packages.append('.'.join([base_name, name]))

    return packages


if __name__ == '__main__':
    print get_tasks_packages()

