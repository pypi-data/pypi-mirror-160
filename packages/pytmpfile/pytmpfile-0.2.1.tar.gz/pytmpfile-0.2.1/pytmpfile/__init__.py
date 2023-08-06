from memory_tempfile import MemoryTempfile
import contextlib
from typing import Optional
import os
import glob
import shutil

__all__ = ['get_tmp_path', 'tempdir']
__version__ = '0.2.1'

SCRATCH_TMP = os.path.join('/scratch', 'tmp', os.environ['SLURM_JOB_ID']) if 'SLURM_JOB_ID' in os.environ else None
PREF_PATH = [SCRATCH_TMP] if SCRATCH_TMP and os.path.exists(SCRATCH_TMP) else []

# Credits: https://pypi.org/project/memory-tempfile/
tempfile = MemoryTempfile(preferred_paths=PREF_PATH + ['/run/user/{uid}'],
                          filesystem_types=['tmpfs', 'ramfs', 'xfs'], fallback=True)

if not tempfile.found_mem_tempdir():
    # raise RuntimeError('No tmp directory found')
    import tempfile


def tempdir():
    return tempfile.gettempdir()


def _get_host_process_id():
    process_id = 'pytmpfile_' + os.uname()[1] + '_' + str(os.getpid())
    return process_id


def _cleanup(path_pattern):
    for path in glob.glob(path_pattern):
        try:
            shutil.rmtree(path)
        except:
            pass


def _write(prefix, suffix, delete, content):
    with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=delete, mode='w+') as ntf:
        if content:
            ntf.write(content)
            ntf.flush()
        yield ntf.name


@contextlib.contextmanager
def get_tmp_path(content: Optional[str] = None, suffix: Optional[str] = None, delete=True) -> str:
    prefix = _get_host_process_id()
    try:
        with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=delete, mode='w+') as ntf:
            if content:
                ntf.write(content)
                ntf.flush()
            yield ntf.name
    except OSError:
        _cleanup(os.path.join(tempdir(), prefix, '*'))
        with tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=delete, mode='w+') as ntf:
            if content:
                ntf.write(content)
                ntf.flush()
            yield ntf.name
