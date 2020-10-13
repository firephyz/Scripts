# Python wrappers over sets of linux tools

import os
import ast
import subprocess
import inspect
import re
import functools

class Toolset:
    config = {}
    abs_paths = {}
    echo_cmd = True
    test = None

    def __init__(self, config, echo=False):
        self.config = config
        self.abs_paths = Toolset.canonicalize(self.config)
        self.echo_cmd = echo
        self.define_hooks()

    # TODO implement 'macro' expansion using ast instead of string source
    # Replace keywords in _hook_name function to create a function specifically
    # for each tool. Remove the standalone calling guard and add code to
    # partially apply self since it isn't technically a class method yet.
    # Eval this new code in an evironment with this instance of self to
    # produce a function able to be called from the class.
    def define_hooks(self):
        for (toolname, toolpath) in list(self.abs_paths.items()):
            # clone hook source for each tool variant
            hook_source = inspect.getsource(self._hook_name)
            # remove leading indents
            hook_source = ''.join(re.findall("    (.*?\n)", hook_source))
            # perform symbol substitution, macro expansion
            hook_source = hook_source.replace("_hook_name", toolname).replace("_cmd_path", toolpath)
            # remove macro exception guard
            exception_guard_regex = "(([\n]|.)*?)    raise Exception\(\"Macro.*?\n(([\n]|.)*)"
            hook_source = ''.join(re.findall(exception_guard_regex, hook_source)[0])
            # add closing code to partially apply self
            hook_source += "gcc = functools.partial({}, self)\n".format(toolname)
            # dynamically create and retrieve function
            macro_env = {'self': self}
            exec(hook_source, None, macro_env)
            function = macro_env[toolname]
            # # add to self instance
            setattr(self, toolname, function)


    def _hook_name(self, args):
        raise Exception("Macro function. Expand and remove exception")
        if self.echo_cmd:
            print("# _hook_name: {args}".format(args=args))
        return subprocess.run(["_cmd_path"] + args.split(' '), check=True, capture_output=True)
        # ret = subprocess.run(["_cmd_path"] + args.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # if ret.returncode != 0:
        #     raise subprocess.CalledProcessError(ret.returncode, "_hook_name", output=ret.stdout, stderr=ret.stderr)
        # return ret


    @staticmethod
    def canonicalize(config):
        path = config['path']
        tools = config['tools']
        def canonicalizer(tool): return [tool[0], "{}/{}".format(path,tool[1])]
        return dict(list(map(canonicalizer, tools.items())))


xgcc = Toolset({'path': '/home/kyle/programs/arm-none-eabi-hard/bin',
                'tools': {'gcc': 'arm-none-eabihf-gcc',
                          'gxx': 'arm-none-eabihf-g++',
                          'ld': 'arm-none-eabihf-ld',
                          'objdump': 'arm-none-eabihf-objdump',
                          'objcopy': 'arm-none-eabihf-objcopy'}},
               echo=True)


if __name__ == "__main__":
    import __main__
    filename = os.path.basename(__main__.__file__)
    raise Exception(
        "{filename} cannot be called as a script.".format(filename=filename))
