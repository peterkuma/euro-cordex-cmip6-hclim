import os
import pickle
import sys
import warnings
from glob import glob

import ds_format as ds

from . import misc


def get_dataset_attrs(filename):
    d = ds.read(filename, [], full=True)
    a = ds.attrs(d)
    a["source"] = misc.get_source_name(a)
    if "period" in a:
        start_year, end_year = a["period"].split("-")
        a["start_year"] = int(start_year)
        a["end_year"] = int(end_year)
    vars = ds.vars(d, full=True)
    for var in misc.VARS:
        if var in vars or var + "_mean" in vars or var + "_mean_ts" in vars:
            a["variable_id"] = var
    return a


def list_dataset_worker(filename):
    try:
        dataset = get_dataset_attrs(filename)
    except Exception as e:
        warnings.warn('cannot read "%s": %s' % (filename, e))
        return
    dataset["filename"] = filename
    return dataset


def list_dataset(dirname, ex=None, force=False):
    if not force:
        index_filename = os.path.join(dirname, "index.pkl")
        try:
            with open(index_filename, "rb") as f:
                return pickle.load(f)
        except IOError:
            pass
    results = []
    orig_dir = os.getcwd()
    os.chdir(dirname)
    files = sorted(glob("**.nc") + glob("**.ds"))
    os.chdir(orig_dir)
    for file in files:
        filename = os.path.join(dirname, file)
        if ex is not None:
            results += [ex.submit(list_dataset_worker, filename)]
        else:
            results += [list_dataset_worker(filename)]
    if ex is not None:
        results = [res.result() for res in results]
    return [res for res in results if res is not None]


def read_dataset(dirname, desc, vars, merge=True, index=None):
    dd = []
    if index is None:
        index = list_dataset(dirname)
    for dataset in index:
        skip = False
        for k, v in desc.items():
            if not (k in dataset and dataset[k] == desc[k]):
                skip = True
        if skip:
            continue
        try:
            d = ds.read(dataset["filename"], vars, jd=True)
        except Exception as e:
            warnings.warn('cannot read "%s": %s' % (dataset["filename"], e))
            continue
        d["filename"] = dataset["filename"]
        dd += [d]
    if merge:
        return ds.merge(dd, "time", new="n")
    else:
        return dd
