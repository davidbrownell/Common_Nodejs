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
from CommonEnvironment import FileSystem
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
    verbose=False,
):
    with StreamDecorator(output_stream).DoneManager(
        line_prefix="",
        prefix="\nResults: ",
        suffix="\n",
    ) as dm:
        npm_install_command_line = "{}{}".format(
            CurrentShell.CreateScriptName("NpmInstall"),
            " /verbose" if verbose else "",
        )

        dm.stream.write("Running 'NpmInstall'...")
        with dm.stream.DoneManager() as this_dm:
            prev_dir = os.getcwd()
            os.chdir(_script_dir)

            with CallOnExit(lambda: os.chdir(prev_dir)):
                this_dm.result = Process.Execute(npm_install_command_line, this_dm.stream)
                if this_dm.result != 0:
                    return this_dm.result

        if os.path.isfile(os.path.join(_script_dir, "src", "package-lock.json")):
            dm.stream.write("Running 'NpmInstall' in 'src'...")
            with dm.stream.DoneManager(
                suffix="\n",
            ) as this_dm:
                prev_dir = os.getcwd()
                os.chdir(os.path.join(_script_dir, "src"))

                with CallOnExit(lambda: os.chdir(prev_dir)):
                    this_dm.result = Process.Execute(npm_install_command_line, this_dm.stream)
                    if this_dm.result != 0:
                        return this_dm.result

        # Look for the bin dir in the path and prompt if it does not exist
        path_dir = os.path.join(_script_dir, "node_modules", ".bin")

        if CurrentShell.HasCaseSensitiveFileSystem:
            query_path_dir = path_dir
            query_decorator_func = lambda path: path
        else:
            query_path_dir = path_dir.lower()
            query_decorator_func = lambda path: path.lower()

        found_path = False

        for existing_path in CurrentShell.EnumEnvironmentVariable("PATH"):
            existing_path = query_decorator_func(existing_path)

            if existing_path == query_path_dir:
                found_path = True
                break

        if not found_path:
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
    output_dir=CommandLine.DirectoryTypeInfo(
        ensure_exists=False,
    ),
    output_stream=None,
)
def Build(
    configuration,
    output_dir,
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

        FileSystem.RemoveTree(output_dir)
        dm.stream.write("Copying content to '{}'...".format(output_dir))
        with dm.stream.DoneManager() as this_dm:
            FileSystem.CopyTree(
                os.path.join(_script_dir, "dist"),
                output_dir,
                optional_output_stream=this_dm.stream,
            )

        return dm.result


# ----------------------------------------------------------------------
@CommandLine.EntryPoint
@CommandLine.Constraints(
    output_dir=CommandLine.DirectoryTypeInfo(
        ensure_exists=False,
    ),
    output_stream=None,
)
def Clean(
    output_dir,
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

        if os.path.isdir(output_dir):
            dm.stream.write("Removing '{}'...".format(output_dir))
            with dm.stream.DoneManager():
                FileSystem.RemoveTree(output_dir)

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
            ),
        ),
    )
    except KeyboardInterrupt:
        pass
