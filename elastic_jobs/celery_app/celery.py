from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

from . import settings

# Must set django configuration to env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apollo.settings.dev")


def get_tasks_packages():
    import os.path

    _packages = []
    tasks_packages_name = 'tasks_pkg'
    base_path = os.path.dirname(os.path.dirname(__file__))

    base_name = os.path.basename(base_path)
    packages_path = os.path.join(base_path, tasks_packages_name)

    for name in os.listdir(packages_path):
        fs_path = os.path.join(packages_path, name)

        if os.path.isdir(fs_path):
            _packages.append('.'.join([base_name, name]))

    return _packages


app = Celery('apollo_celery_app')

# Using a string here means the worker don't have to serialize the configuration object to child processes.
# Notice: namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# ************************************************************************************************* #
# *  If set namespace parameter, must use `elastic_jobs.settings:dj_settings`config,              * #
# *  otherwise celery app don't load config when launch `celery worker` command.                  * #
# *                                                                                               * #
# *  ******: from . import dj_settings                                                            * #
# *  ******: app = Celery('dj_celery_tasks')                                                      * #
# *  ******: app.config_from_object(dj_settings, namespace='DJ_CELERY')                           * #
# ************************************************************************************************* #

app.autodiscover_tasks(packages=get_tasks_packages())


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
