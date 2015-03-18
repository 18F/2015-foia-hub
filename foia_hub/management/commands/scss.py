from glob import glob
import os
import subprocess
import optparse

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = """Runs the sass executable to compile the scss. Add parameter
    "watch" to kick off a demon"""


    option_list = BaseCommand.option_list + (
        optparse.make_option(
            "--style",
            dest="style",
            default="nested",
            help="specify the CSS output style: 'nested', 'expanded' (default), 'compact', or 'compressed'"
        ),
    )

    def handle(self, *args, **options):
        self.style = options["style"]
        if args and args[0] == 'watch':
            self.watch()
        else:
            self.compile()

    def compile(self):
        """Cycle through each scss file, compiling them one by one"""
        static = os.path.join("foia_hub", "static")
        for path in glob(os.path.join(static, "sass", "*.scss")):
            filename = path.split(os.path.sep)[-1][:-5]
            if filename[0] == "_":
                continue
            subprocess.call(["sass", "--style", self.style, "--scss", path,
                             os.path.join(static, "css", filename + ".css")])

    def watch(self):
        """Kick off the 'watch' demon"""
        watch_path = os.path.join("foia_hub", "static", "sass")
        watch_path += ":"
        watch_path += os.path.join("foia_hub", "static", "css")
        subprocess.call(["sass", "--style", self.style, "--scss", "--watch",
                         watch_path])
