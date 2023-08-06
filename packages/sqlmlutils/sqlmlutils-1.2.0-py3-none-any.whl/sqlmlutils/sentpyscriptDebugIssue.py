import sys
from io import StringIO
from pandas import DataFrame

_temp_out = StringIO()
_temp_err = StringIO()

sys.stdout = _temp_out
#sys.stderr = _temp_err
OutputDataSet = DataFrame()


def get_server_info():
    from distutils.version import LooseVersion
    import pip, sysconfig
    pipversion = LooseVersion(pip.__version__)

    if pipversion >= LooseVersion("19.3"):
        from wheel import pep425tags
    elif pipversion > LooseVersion("10"):
        from pip._internal import pep425tags
    else:
        from pip import pep425tags
    return {
        "impl_version_info": pep425tags.get_impl_version_info(), #(3,7)
        "abbr_impl": pep425tags.get_abbr_impl(), #''cp''
        "abi_tag": pep425tags.get_abi_tag(), #''cp37m''
        "platform": sysconfig.get_platform().replace("-","_") #''win_amd64'', ''linux_x86_64''
    }
 
        
import dill

# serialized keyword arguments
args_dill = bytes.fromhex("80047d942e")
# serialized positional arguments
pos_args_dill = bytes.fromhex("8004292e")

args = dill.loads(args_dill)
pos_args = dill.loads(pos_args_dill)

# user function name
func = get_server_info
    
# call user function with serialized arguments
return_val = func(*pos_args, **args)

# serialize results of user function and put in DataFrame for return through SQL Satellite channel
OutputDataSet["return_val"] = [dill.dumps(return_val).hex()]

#myErrValue = _temp_err.getvalue()
OutputDataSet["_stdout_"] = [_temp_out.getvalue()]
#OutputDataSet["_stderr_"] = [_temp_err.getvalue()]