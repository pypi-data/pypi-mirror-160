"""Git abstraction
"""

from subprocess import PIPE, Popen


class GitCommandError(Exception):
    """Raised when git command returns non-zero value"""

    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(f"stdout: {stdout}\nstderr: {stderr}")


class Git:
    """A git helper abstraction"""

    def __init__(self, path: str):
        self.path = path
        self.returncode = -1

    def execute(self, subcmd, *args, **kwargs) -> str:
        """Execute a subcommand of git"""
        arglist = ["git", subcmd, *args]
        for argument, value in kwargs.items():
            arglist.extend((f"--{argument.replace('_', '-')}", value))
        fid = Popen(arglist, cwd=self.path, stdout=PIPE, stderr=PIPE)
        out, err = fid.communicate()
        self.returncode = fid.returncode
        if fid.returncode != 0:
            raise GitCommandError(out.decode("utf-8"), err.decode("utf-8"))
        return out.decode("utf-8").strip()
