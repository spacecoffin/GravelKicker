# Standard Python library imports
import hashlib

# Scientific computing library imports
import numpy as np
import pandas as pd
from scipy import stats

# Supriya imports
from supriya.tools import synthdeftools
from supriya.tools import ugentools

# DSP imports
import librosa

__all__ = ['cp_to_sc', 'build_out', 'format_params', 'gen_min_max_freq', 
           'gen_params', 'make_builder']


def gen_min_max_freq(size=1, lambda_=0.7):
    """Returns randomly generated min and max freqs for a Gendyn oscillator"""

    def min_gen(a):
        """Generate a random int between 0 & a (inclusive) of a 1-D array"""
        return np.random.randint(0, a+1, size=1)
    
    # Vectorize function so it can be applied to array
    min_func = np.vectorize(min_gen)
    
    octave_range = stats.planck.rvs(lambda_, size=size)
    note_range = np.random.randint(1, 13, size=size)
    total_range = np.clip(octave_range, 0, 8)*12 + note_range
    base_note = min_func(110-total_range)
    
    m_arr = np.append(base_note, base_note+total_range)
    
    return librosa.core.midi_to_hz(m_arr).reshape(2, size).T


def gen_params(dists=False, rows=1, lambda_=0.7, M=100, n=12, N=65):
    """Generate a numpy matrix of parameters for Gendyn synths"""

    param_and_scale_arr = np.random.uniform(low=0.0001, 
                                            high=1.0, 
                                            size=4*rows).reshape(rows, 4)

    if dists:
        _amp_dist, _dur_dist = dists
        dist_arr = np.tile([_amp_dist, _dur_dist], rows).reshape(rows, 2)
    else:
        dist_arr = np.random.randint(6, size=2*rows).reshape(rows, 2)

    knum_arr = (stats.hypergeom.rvs(M=M, 
                                n=n, 
                                N=N, 
                                size=1*rows)+4).reshape(rows, 1)

    init_cp_arr = (np.zeros(rows)+16).reshape(rows, 1)
    
    return np.concatenate([param_and_scale_arr,
                           dist_arr,
                           knum_arr,
                           gen_min_max_freq(size=rows, lambda_=lambda_),
                           init_cp_arr],
                           axis=1)


def format_params(param_mtx):
    
    cols = ('adparam', 'ampscale', 'ddparam', 'durscale', 'ampdist', 'durdist', 
            'knum', 'minfrequency', 'maxfrequency', 'init_cps')
    
    _df = pd.DataFrame(param_mtx, columns=cols)

    _md5 = [hashlib.md5(series.tostring()).hexdigest() for series in param_mtx]
    
    _df["hash"] = np.array(_md5)
    
    return _df


def cp_to_sc(r):
    """Print row of param mtx in the order an SC Gendy1 wants them."""
    print("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(r["ampdist"],
                                                          r["durdist"],
                                                          r["adparam"],
                                                          r["ddparam"],
                                                          r["minfrequency"],
                                                          r["maxfrequency"],
                                                          r["ampscale"],
                                                          r["durscale"],
                                                          r["init_cps"],
                                                          r["knum"]))


def make_builder(row):
    return synthdeftools.SynthDefBuilder(adparam=row["adparam"],
                                         ampdist=row["ampdist"],
                                         ampscale=row["ampscale"],
                                         ddparam=row["ddparam"],
                                         durdist=row["durdist"],
                                         durscale=row["durscale"],
                                         init_cps=row["init_cps"],
                                         knum=row["knum"],
                                         maxfrequency=row["maxfrequency"],
                                         minfrequency=row["minfrequency"],
                                        )


def build_out(builder):
    
    with builder:
        return ugentools.Out.ar(
            source=ugentools.Gendy1.ar(
                adparam=builder['adparam'],
                ampdist=builder['ampdist'],
                ampscale=builder['ampscale'],
                ddparam=builder['ddparam'],
                durdist=builder['durdist'],
                durscale=builder['durscale'],
                init_cps=builder['init_cps'],
                knum=builder['knum'],
                maxfrequency=builder['maxfrequency'],
                minfrequency=builder['minfrequency'],
            )
            )


