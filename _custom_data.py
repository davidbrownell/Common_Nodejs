# ----------------------------------------------------------------------
# |
# |  _custom_data.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2020-03-06 11:56:34
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2020-21
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Data used by both Setup_custom.py and Activate_custom.py"""

import os

import CommonEnvironment
from CommonEnvironment.Shell.All import CurrentShell

# ----------------------------------------------------------------------
_script_fullpath                            = CommonEnvironment.ThisFullpath()
_script_dir, _script_name                   = os.path.split(_script_fullpath)
# ----------------------------------------------------------------------

if CurrentShell.CategoryName == "Windows":
    _CUSTOM_DATA                            = [
        (
            "Nodejs - 12.16.1",
            "4e538eac2fc90225fbe6d2be3c09e87b97baf8389056e4c09757204d96eeb9df",
            [
                "Tools",
                "Nodejs",
                "v12.16.1",
                "Windows",
            ],
        ),
    ]

elif CurrentShell.CategoryName == "Linux":
    _CUSTOM_DATA                            = [
        (
            "Nodejs - 12.16.1",
            "6c9c4f96d967acab7b01086894efc51d0f2d6f288ceac11e8b9b554aedf7f376",
            [
                "Tools",
                "Nodejs",
                "v12.16.1",
                "Linux",
            ],
        ),
    ]

elif CurrentShell.CategoryName == "BSD":
    _CUSTOM_DATA                            = [
        (
            "Nodejs - 12.16.1",
            "75288b2a995b74849561644a883280fc3b2be99c83d93849fd4f0d362d8c0261",
            [
                "Tools",
                "Nodejs",
                "v12.16.1",
                "BSD",
            ],
        ),
    ]

else:
    raise Exception("'{}' is not supported".format(CurrentShell.CategoryName))
