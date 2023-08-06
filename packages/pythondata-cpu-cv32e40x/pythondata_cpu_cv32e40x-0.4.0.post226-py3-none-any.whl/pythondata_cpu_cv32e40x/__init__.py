import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post226"
version_tuple = (0, 4, 0, 226)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post226")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post84"
data_version_tuple = (0, 4, 0, 84)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post84")
except ImportError:
    pass
data_git_hash = "263b2093b90ad48f81efba8b0a9221da9cf9f7b8"
data_git_describe = "0.4.0-84-g263b2093"
data_git_msg = """\
commit 263b2093b90ad48f81efba8b0a9221da9cf9f7b8
Merge: 5ecb42b7 48d60fee
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Jul 26 11:54:49 2022 +0200

    Merge pull request #626 from Silabs-ArjanB/ArjanB_u1
    
    Unifying code with CV32E40S

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
