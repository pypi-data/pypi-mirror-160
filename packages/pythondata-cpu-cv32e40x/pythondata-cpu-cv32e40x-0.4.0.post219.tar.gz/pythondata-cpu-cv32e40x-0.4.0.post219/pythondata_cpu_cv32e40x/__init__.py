import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post219"
version_tuple = (0, 4, 0, 219)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post219")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post77"
data_version_tuple = (0, 4, 0, 77)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post77")
except ImportError:
    pass
data_git_hash = "b4963169df0a7480e1130a4265e1be97ace5c12d"
data_git_describe = "0.4.0-77-gb4963169"
data_git_msg = """\
commit b4963169df0a7480e1130a4265e1be97ace5c12d
Merge: d542e41c dc11672f
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Jul 20 18:53:43 2022 +0200

    Merge pull request #625 from Silabs-ArjanB/ArjanB_zc705
    
    Updated Zc extension version to v0.70.5

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
