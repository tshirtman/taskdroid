# coding: utf-8
from os import environ
from subprocess import Popen
from os.path import expanduser

from kivy.app import App
from kivy.properties import ListProperty
from kivy.utils import platform

from tasklib.backends import TaskWarrior
from tasklib.filters import TaskWarriorFilter

__version__ = '0.1'


if platform == 'android':
    Popen(['chmod', '755', 'task'])
    Popen(['ls', '-l'])
    environ['LD_LIBRARY_PATH'] = 'libs/android/'
    environ['PATH'] += ':.'

    TW = TaskWarrior(taskrc_location='/sdcard/taskrc')
else:
    TW = TaskWarrior(taskrc_location=expanduser('~/.task/taskrc'))


# register garden.recycleview
from kivy.garden.recycleview import RecycleView  # noqa


class TaskDroid(App):
    filters = ListProperty()
    tasks = ListProperty()

    def build(self):
        super(TaskDroid, self).build()
        self.refresh_tasks()

    def refresh_tasks(self, *args):
        F = TaskWarriorFilter(TW)
        for f in self.filters:
            F.add_filter_param(*f)

        self.tasks = []
        for t in TW.filter_tasks(F):
            self.tasks.append({
                'text': 'proj:{p}, tags:{t}, {s}'.format(
                    p=t['project'], t=t['tags'], s=str(t)),
                'task': t
                })

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = TaskDroid()
    app.run()
