import numpy as np
import pandas as pd
import librosa

__all__ = ['featurize', 'get_stats']


def get_stats(y):
    _mean = np.mean(y.T, axis=0)
    _min = np.amin(y.T, axis=0)
    _max = np.amax(y.T, axis=0)
    _var = np.var(y.T, axis=0)

    if y.ndim < 2:
        return {"mean": _mean,
                "min": _min,
                "max": _max,
                "var": _var}

    else:
        # And the first-order & second-order differences (delta features)
        dy = librosa.feature.delta(y)
        d2y = librosa.feature.delta(y, order=2)

        _dmean = np.mean(dy.T, axis=0)
        _dvar = np.var(dy.T, axis=0)
        _d2mean = np.mean(d2y.T, axis=0)
        _d2var = np.var(d2y.T, axis=0)

    return {"min": _min,
            "max": _max,
            "mean": _mean,
            "dmean": _dmean,
            "dmean2": _d2mean,
            "var": _var,
            "dvar": _dvar,
            "dvar2": _d2var,}


# Regular audio time series in
# Non-dict outputs (summary features, spectral features) tuple
# Output formats: "dict", "df" for DataFrame, "np" for np.array
# If out=="np" && concat==True, summary and spectral stats are returned as a single array.
def featurize(y, sr=44100, out="np", concat=True):
    # Normalize amplitude values of y
    # TODO: Should we only normalize when there is an out of bounds value, i.e. check first?
    _y_normed = librosa.util.normalize(y)
    _mfcc = librosa.feature.mfcc(y=_y_normed, sr=sr, n_mfcc=13)
    _cent = np.mean(librosa.feature.spectral_centroid(y=_y_normed, sr=sr))

    _stat_dict = get_stats(_mfcc)

    if out == "dict":
        _stat_dict["cent"] = _cent
        return _stat_dict

    else:
        _spec_stat_df = pd.DataFrame(_stat_dict)

    _sum_stats = _cent

    if out == "df":
        # _spec_stat_df = pd.DataFrame(_stat_dict)
        return _sum_stats, _spec_stat_df

    else:

        _spec_stat_np = _spec_stat_df.as_matrix().T.flatten()

        if not concat:
            return _sum_stats, _spec_stat_np

        return np.append(_sum_stats, _spec_stat_np)
