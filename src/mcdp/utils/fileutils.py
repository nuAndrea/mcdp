from contextlib import contextmanager

        
def get_mcdp_tmp_dir():
    from tempfile import gettempdir
    import os
    d0 = gettempdir()
    d = os.path.join(d0, 'mcdp_tmp_dir')
    if not os.path.exists(d):
        os.makedirs(d)
    return d

@contextmanager
def tmpfile(suffix):
    """ Yields the name of a temporary file """
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
    yield temp_file.name
    temp_file.close()