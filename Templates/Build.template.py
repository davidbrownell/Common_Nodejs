# ----------------------------------------------------------------------
# |
# |  Build.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2020-03-14 12:15:05
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2020
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Builds the current website using gulp"""

import os
import sys
import textwrap

import six

import CommonEnvironment
from CommonEnvironment import BuildImpl
from CommonEnvironment.CallOnExit import CallOnExit
from CommonEnvironment import CommandLine
from CommonEnvironment import Process
from CommonEnvironment.Shell.All import CurrentShell
from CommonEnvironment.StreamDecorator import StreamDecorator

# ----------------------------------------------------------------------
_script_fullpath = CommonEnvironment.ThisFullpath()
_script_dir, _script_name = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

PROJECT_NAME                                = "<Project Name>"

raise Exception("Remove this exception once the configuration settings above have been updated for your project")

CONFIGURATIONS                              = ["debug", "release"]

StreamDecorator.InitAnsiSequenceStreams()

# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    output_stream=None,
)
def Setup(
    output_stream=sys.stdout,
):
    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        dm.stream.write("Running 'NpmInstall'...")
        with dm.stream.DoneManager() as this_dm:
            prev_dir = os.getcwd()
            os.chdir(_script_dir)

            with CallOnExit(lambda: os.chdir(prev_dir)):
                this_dm.result = Process.Execute(CurrentShell.CreateScriptName("NpmInstall"), this_dm.stream)
                if this_dm.result != 0:
                    return this_dm.result

        path_dir = os.path.join(_script_dir, "node_modules", ".bin")

        dm.stream.write(
            textwrap.dedent(
                """\

                Node dependencies have been installed. Please make sure to add this value
                to your path:

                    {path_dir}

                    Using the command:
                        {instructions}

                """,
            ).format(
                path_dir=path_dir,
                instructions=CurrentShell.GenerateCommands(
                    CurrentShell.Commands.AugmentPath(
                        path_dir,
                        append_values=True,
                        simple_format=True,
                    ),
                ),
            ),
        )

        return dm.result


# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    configuration=CommandLine.EnumTypeInfo(CONFIGURATIONS),
    output_stream=None,
)
def Build(
    configuration,
    output_stream=sys.stdout,
):
    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        command_line = "gulp build{}".format(
            " --release" if configuration == "release" else "",
        )

        dm.stream.write("Building via '{}'...".format(command_line))
        with dm.stream.DoneManager() as this_dm:
            prev_dir = os.getcwd()
            os.chdir(_script_dir)

            with CallOnExit(lambda: os.chdir(prev_dir)):
                this_dm.result = Process.Execute(command_line, this_dm.stream)
                if this_dm.result != 0:
                    return this_dm.result

        return dm.result


# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    output_stream=None,
)
def Clean(
    output_stream=sys.stdout,
):
    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        dm.stream.write("Cleaning via 'gulp clean'...")
        with dm.stream.DoneManager() as this_dm:
            prev_dir = os.getcwd()
            os.chdir(_script_dir)

            with CallOnExit(lambda: os.chdir(prev_dir)):
                this_dm.result = Process.Execute("gulp clean", this_dm.stream)
                if this_dm.result != 0:
                    return this_dm.result

        return dm.result


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try: sys.exit(
        BuildImpl.Main(
            BuildImpl.Configuration(
                PROJECT_NAME,
                configurations=CONFIGURATIONS,
                configuration_required_on_clean=False,
                requires_output_dir=False,
            ),
        ),
    )
    except KeyboardInterrupt:
        pass
