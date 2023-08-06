import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post228"
version_tuple = (0, 4, 0, 228)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post228")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post86"
data_version_tuple = (0, 4, 0, 86)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post86")
except ImportError:
    pass
data_git_hash = "d0fa78738c2e2dced07e3969db2edef6b211313c"
data_git_describe = "0.4.0-86-gd0fa7873"
data_git_msg = """\
commit d0fa78738c2e2dced07e3969db2edef6b211313c
Merge: 263b2093 fc5301d1
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Jul 26 14:11:57 2022 +0200

    Merge pull request #627 from Silabs-ArjanB/ArjanB_235
    
    Updated exception code for Instruction Bus Fault

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
