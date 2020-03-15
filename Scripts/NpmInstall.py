# ----------------------------------------------------------------------
# |
# |  NpmInstall.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2020-03-06 18:09:07
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2020
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Installs node modules via npm with only a package-lock.json file"""

import json
import os
import sys

import six

import CommonEnvironment
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import FileSystem
from CommonEnvironment import Process
from CommonEnvironment.StreamDecorator import StreamDecorator

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

@CommandLine.EntryPoint
@CommandLine.Constraints(
    working_dir=CommandLine.DirectoryTypeInfo(
        arity="?",
    ),
    output_stream=None,
)
def EntryPoint(
    working_dir=os.getcwd(),
    preserve_package=False,
    output_stream=sys.stdout,
    verbose=False,
):
    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        prev_dir = os.getcwd()

        os.chdir(working_dir)
        with CallOnExit(lambda: os.chdir(prev_dir)):
            dm.stream.write("Reading 'package-lock.json'...")
            with dm.stream.DoneManager() as this_dm:
                if not os.path.isfile("package-lock.json"):
                    this_dm.stream.write("ERROR: 'package-lock.json' does not exist.\n")
                    this_dm.result = -1

                    return this_dm.result

                with open("package-lock.json") as f:
                    content = json.load(f)

                if "dependencies" not in content:
                    this_dm.stream.write("ERROR: 'dependencies' was not found.\n")
                    this_dm.result = -1

                    return this_dm.result

                dependencies = content["dependencies"]

            dm.stream.write("Creating 'package.json'...")
            with dm.stream.DoneManager() as this_dm:
                if os.path.isfile("package.json"):
                    os.rename("package.json", "package.json.old")
                    restore_file_func = lambda: os.rename("package.json.old", "package.json")
                else:
                    restore_file_func = lambda: None

                for k, v in dependencies.items():
                    dependencies[k] = "={}".format(v["version"])

                with open("package.json", "w") as f:
                    json.dump(
                        {
                            "dependencies": dependencies,
                        },
                        f,
                    )

        with CallOnExit(restore_file_func):
            if preserve_package:
                remove_file_func = lambda: None
            else:
                remove_file_func = lambda: FileSystem.RemoveFile("package.json")

            with CallOnExit(remove_file_func):
                dm.stream.write("Running 'npm ci'...")
                with dm.stream.DoneManager() as this_dm:
                    if verbose:
                        this_output_stream = this_dm.stream
                    else:
                        this_output_stream = six.moves.StringIO()

                    this_dm.result = Process.Execute("npm ci", this_output_stream)
                    if this_dm.result != 0:
                        if not verbose:
                            this_dm.stream.write(this_output_stream.getvalue())

                        return this_dm.result

        return dm.result


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sys.exit(
            CommandLine.Main()
        )
    except KeyboardInterrupt:
        pass
