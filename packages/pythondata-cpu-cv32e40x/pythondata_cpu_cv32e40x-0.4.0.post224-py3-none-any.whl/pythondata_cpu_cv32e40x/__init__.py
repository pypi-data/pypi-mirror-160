import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post224"
version_tuple = (0, 4, 0, 224)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post224")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post82"
data_version_tuple = (0, 4, 0, 82)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post82")
except ImportError:
    pass
data_git_hash = "5ecb42b7caf94c157c90fe71d2ffc9b60c78bb44"
data_git_describe = "0.4.0-82-g5ecb42b7"
data_git_msg = """\
commit 5ecb42b7caf94c157c90fe71d2ffc9b60c78bb44
Merge: b4963169 7de0e27f
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Thu Jul 21 13:56:07 2022 +0200

    Merge pull request #580 from michael-platzer/xif_update
    
    Update XIF interface

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
