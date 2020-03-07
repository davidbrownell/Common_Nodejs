# ----------------------------------------------------------------------
# |
# |  Setup_custom.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2018-05-03 22:12:13
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2018-20.
# |  Distributed under the Boost Software License, Version 1.0.
# |  (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
# |
# ----------------------------------------------------------------------
"""Performs repository-specific setup activities."""

# ----------------------------------------------------------------------
# |
# |  To setup an environment, run:
# |
# |     Setup(.cmd|.ps1|.sh) [/debug] [/verbose] [/configuration=<config_name>]*
# |
# ----------------------------------------------------------------------

import os
import sys

from collections import OrderedDict

import CommonEnvironment
from CommonEnvironment import FileSystem

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

# <Missing function docstring> pylint: disable = C0111
# <Line too long> pylint: disable = C0301
# <Wrong hanging indentation> pylint: disable = C0330
# <Class '<name>' has no '<attr>' member> pylint: disable = E1103
# <Unreachable code> pylint: disable = W0101
# <Wildcard import> pylint: disable = W0401
# <Unused argument> pylint: disable = W0613

fundamental_repo                                                            = os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL")
assert os.path.isdir(fundamental_repo), fundamental_repo

sys.path.insert(0, fundamental_repo)
from RepositoryBootstrap import *                                           # <Unused import> pylint: disable = W0614
from RepositoryBootstrap.SetupAndActivate import CurrentShell               # <Unused import> pylint: disable = W0614
from RepositoryBootstrap.SetupAndActivate.Configuration import *            # <Unused import> pylint: disable = W0614

del sys.path[0]

from _custom_data import CUSTOM_DATA

# ----------------------------------------------------------------------
# There are two types of repositories: Standard and Mixin. Only one standard
# repository may be activated within an environment at a time while any number
# of mixin repositories can be activated within a standard repository environment.
# Standard repositories may be dependent on other repositories (thereby inheriting
# their functionality), support multiple configurations, and specify version
# information for tools and libraries in themselves or its dependencies.
#
# Mixin repositories are designed to augment other repositories. They cannot
# have configurations or dependencies and may not be activated on their own.
#
# These difference are summarized in this table:
#
#                                                       Standard  Mixin
#                                                       --------  -----
#      Can be activated in isolation                       X
#      Supports configurations                             X
#      Supports VersionSpecs                               X
#      Can be dependent upon other repositories            X
#      Can be activated within any other Standard                  X
#        repository
#
# Consider a script that wraps common Git commands. This functionality is useful
# across a number of different repositories, yet doesn't have functionality that
# is useful on its own; it provides functionality that augments other repositories.
# This functionality should be included within a repository that is classified
# as a mixin repository.
#
# To classify a repository as a Mixin repository, decorate the GetDependencies method
# with the MixinRepository decorator.
#


# @MixinRepository # <-- Uncomment this line to classify this repository as a mixin repository
def GetDependencies():
    """
    Returns information about the dependencies required by this repository.

    The return value should be an OrderedDict if the repository supports multiple configurations
    (aka is configurable) or a single Configuration if not.
    """

    return Configuration(
        "Standard configuration",
        [
            Dependency(
                "0EAA1DCF22804F90AD9F5A3B85A5D706",
                "Common_Environment",
                "python36",
                "https://github.com/davidbrownell/Common_Environment_v3.git",
            ),
        ],
    )


# ----------------------------------------------------------------------
def GetCustomActions(debug, verbose, explicit_configurations):
    """
    Returns an action or list of actions that should be invoked as part of the setup process.

    Actions are generic command line statements defined in
    <Common_Environment>/Libraries/Python/CommonEnvironment/v1.0/CommonEnvironment/Shell/Commands/__init__.py
    that are converted into statements appropriate for the current scripting language (in most
    cases, this is Bash on Linux systems and Batch or PowerShell on Windows systems.
    """

    actions = []

    for name, version, path_parts in CUSTOM_DATA:
        this_dir = os.path.join(*[_script_dir] + path_parts)
        assert os.path.isdir(this_dir), this_dir

        install_filename = os.path.join(this_dir, "Install.7z")
        assert os.path.isfile(install_filename), install_filename

        # Install the file
        actions += [
            CurrentShell.Commands.Execute(
                'python "{script}" Install "{name}" "{uri}" "{dir}" "/unique_id={version}" /unique_id_is_hash'.format(
                    script=os.path.join(
                        os.getenv("DEVELOPMENT_ENVIRONMENT_FUNDAMENTAL"),
                        "RepositoryBootstrap",
                        "SetupAndActivate",
                        "AcquireBinaries.py",
                    ),
                    name=name,
                    uri=FileSystem.FilenameToUri(
                        install_filename,
                    ).replace("%", "%%"),
                    dir=this_dir,
                    version=version,
                ),
            ),
        ]

    return actions
