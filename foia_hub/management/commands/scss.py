from glob import glob
import os
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """Runs the sass executable to compile the scss. Add parameter
    "watch" to kick off a demon"""

    def handle(self, *args, **options):
        if args and args[0] == 'watch':
            self.watch()
        else:
            self.compile()

    def compile(self):
        """Cycle through each scss file, compiling them one by one"""
        static = os.path.join("foia_hub", "static")
        for path in glob(os.path.join(static, "sass", "*.scss")):
            filename = path.split(os.path.sep)[-1][:-5]
            subprocess.call(["sass", "--style", "expanded", "--scss", path,
                             os.path.join(static, "css", filename + ".css")])

    def watch(self):
        """Kick off the 'watch' demon"""
        watch_path = os.path.join("foia_hub", "static", "sass")
        watch_path += ":"
        watch_path += os.path.join("foia_hub", "static", "css")
        subprocess.call(["sass", "--style", "expanded", "--scss", "--watch",
                         watch_path])
