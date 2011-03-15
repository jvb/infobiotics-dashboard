from os import devnull

class Silence():
    """Context manager which uses low-level file descriptors to suppress
    output to stdout/stderr, optionally redirecting to the named file(s).
    
    >>> with Silence():
    ...     foo = 123 + 456
    ...     print "foo =", foo
    ...
    >>> foo
    579
    >>>
    """
    def __init__(self, stdout=devnull, stderr=devnull, mode="a+"):
        import sys, os
        self.sys, self.os = sys, os
        self.outfiles = stdout, stderr
        self.combine = (stdout == stderr)
        self.mode = mode
    def __enter__(self):
        sys, os = self.sys, self.os
        # save previous stdout/stderr
        self.saved_streams = saved_streams = sys.stdout, sys.stderr
        self.fds = fds = [s.fileno() for s in saved_streams]
        self.saved_fds = map(os.dup, fds)
        
        # open surrogate files
        if self.combine: null_streams = [open(self.outfiles[0], self.mode)] * 2
        else: null_streams = [open(f, self.mode) for f in self.outfiles]
        self.null_fds = null_fds = [s.fileno() for s in null_streams]
        sys.stdout, sys.stderr = self.null_streams = null_streams
        
        # overwrite low-level file descriptors
        map(os.dup2, null_fds, fds)
    def __exit__(self, *args):
        sys, os = self.sys, self.os
        # restore original stdout/stderr and fds
        map(os.dup2, self.saved_fds, self.fds)
        for s in self.null_streams: 
            s.close()
            if self.combine: break
        sys.stdout, sys.stderr = self.saved_streams
        return False
