import os

__all__ = ['get_cwd_parent_dir', 'join_path_to_file', 'make_out_dirs']


def get_cwd_parent_dir():
    """Return abs path of cwd's parent dir"""
    return os.path.split(os.getcwd())[0]


def join_path_to_file(osc_p, aif_p, f):
    osc_fp = os.path.join(osc_p, f) + ".osc"
    aif_fp = os.path.join(aif_p, f) + ".aiff"
    return osc_fp, aif_fp


def make_out_dirs(path):
    if os.path.exists(path):
        of = os.path.join(path, "osc_files")
        af = os.path.join(path, "aif_files")
        os.makedirs(of, exist_ok=True)
        os.makedirs(af, exist_ok=True)
        return of, af
    else:
        return "{} does not exist".format(path)

