# coding: utf-8
__version__ = '0.1'

from shlex import split
from subprocess import Popen, PIPE
from threading import Thread

from kivy.app import App
from kivy.properties import BooleanProperty, ListProperty
from kivy.utils import platform

if platform == 'android':
    TASK = './task'
else:
    TASK = 'task'

# register garden.recycleview
from kivy.garden.recycleview import RecycleView  # noqa


class TaskDroid(App):
    lock = BooleanProperty(False)
    output = ListProperty([])

    def build(self):
        super(TaskDroid, self).build()
        for i in range(10):
            print "!" * 30 + " START " + "!" * 30
        print "chmod"
        Popen(['chmod', '755', 'task'])
        Popen(['ls', '-l'])
        print "done"

    def run_task(self, args):
        if self.lock:
            return
        Thread(target=self._run_task, args=[args]).start()

    def _run_task(self, args):
        self.lock = True
        #p = Popen([TASK] + split(args), stdout=PIPE)
        self.output.append({'text': '_' * 80})
        self.output.append({'text': args})

        p = Popen(split(args), stdout=PIPE, stderr=PIPE)
        for l in p.stdout.readlines():
            self.output.append({'text': l})
        for l in p.stderr.readlines():
            self.output.append({'text': l})
        self.lock = False

if __name__ == '__main__':
    app = TaskDroid()
    app.run()
