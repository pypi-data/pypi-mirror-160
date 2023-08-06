import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post230"
version_tuple = (0, 4, 0, 230)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post230")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post88"
data_version_tuple = (0, 4, 0, 88)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post88")
except ImportError:
    pass
data_git_hash = "4f7a8d912091bb4f54cbd3e25761f495c27a7aaa"
data_git_describe = "0.4.0-88-g4f7a8d91"
data_git_msg = """\
commit 4f7a8d912091bb4f54cbd3e25761f495c27a7aaa
Merge: d0fa7873 19d836f3
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Jul 27 11:14:33 2022 +0200

    Merge pull request #631 from Silabs-ArjanB/ArjanB_clicbm
    
    Fixed bitfield description in mtvec CSR for CLIC

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
