import subprocess
from .os import join_path_to_file
from .os import make_out_dirs
#from supriya.tools import nonrealtimetools

__all__ = ['make_cmd', 'make_osc_file', 'render_session']


def make_cmd(osc_fp, aif_fp):
    return "scsynth -N {0} _ {1} 44100 AIFF int16 -o 1".format(osc_fp, aif_fp)


def make_osc_file(session, fpath):
    datagram = session.to_datagram()
    with open(fpath, 'wb') as file_pointer:
        file_pointer.write(datagram)


def render_session(session, out_dir, fname):
    osc_path, aif_path = make_out_dirs(out_dir)
    osc_fpath, aif_fpath = join_path_to_file(osc_path, aif_path, fname)
    make_osc_file(session, osc_fpath)
    bashCommand = make_cmd(osc_fpath, aif_fpath)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error