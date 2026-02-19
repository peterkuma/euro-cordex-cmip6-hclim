import calendar
import os
import re

import aquarius_time as aq
import ds_format as ds
import numpy as np

SOURCE_PREFIX = {
    "HCLIM43-ALADIN": "HC",
}

REGIONS = {
    # code: name, lon1, lon2, lat1, lat2
    "BI": ["British Isles", -10, 2, 50, 59],
    "IP": ["Iberian Peninsula", -10, 3, 36, 44],
    "FR": ["France", -5, 5, 44, 50],
    "ME": ["Mid-Europe", 2, 16, 48, 55],
    "SC": ["Scandinavia", 5, 30, 55, 70],
    "AL": ["Alps", 5, 15, 44, 48],
    "MD": ["Mediterranean", 3, 25, 36, 44],
    "EA": ["Eastern Europe", 16, 30, 44, 55],
}

VARS = [
    "pr",
    "psl",
    "tas",
    "tasmax",
    "tasmin",
]

UNITS_PRETTY = {
    "degree_C": "°C",
    "year-1": "yr$^{-1}$",
    "decade-1": "decade$^{-1}$",
    "mon-1": "mon$^{-1}$",
}


def get_source_name(a):
    if "domain_id" in a:
        eid = a.get("driving_experiment_id", a.get("experiment_id"))
        eid = eid.lower() if eid is not None else None
        x = [
            a["domain_id"],
            a["driving_source_id"],
            eid,
            a["driving_variant_label"],
            a.get("institution_id", a.get("institute_id")),
            a["source_id"],
            a.get("version_realization", "v1-r1"),
            a["frequency"],
        ]
    else:
        x = [
            a["source_id"],
            a["experiment_id"].lower(),
            a.get("variant_label", a.get("driving_variant_label")),
        ]
    return "_".join(x)


def get_source_title(attrs):
    sid = attrs.get("source_id")
    did = attrs.get("driving_source_id")
    if did == "REAN" or did is None:
        return sid
    elif did in ["OBS", "ENS"]:
        return did
    else:
        prefix = SOURCE_PREFIX.get(sid, sid)
        return prefix + "/" + did


def get_pretty_units(x):
    parts = x.split(" ")
    return " ".join([UNITS_PRETTY.get(part, part) for part in parts])


def get_pretty_var_label(long_name):
    return (
        long_name.capitalize()
        .replace(" monthly mean", "")
        .replace("minimum", "min.")
        .replace("maximum", "max.")
        .replace("temperature", "temp.")
    )


def convert_pretty_units(x, units):
    parts = units.split(" ")
    if parts[:3] == ["kg", "m-2", "s-1"]:
        x = x * 3600
        parts = ["mm", "h-1"] + parts[3:]
    if parts[:2] == ["mm", "h-1"]:
        x = x * 24 * (365.2425 / 12)
        parts[1] = "mon-1"
    if parts == ["K", "year-1"]:
        parts[0] = "degree_C"
    if parts[0] == "Pa":
        x = x * 1e-2
        parts[0] = "hPa"
    if parts[-1] == "year-1":
        x = x * 10
        parts[-1] = "decade-1"
    return x, " ".join(parts)


def normalize_monthly_time(time):
    date = aq.to_date(time)
    year, month = date[1], date[2]
    mdays = np.array(
        [calendar.monthrange(y, m)[1] for y, m in zip(year, month)]
    )
    day = mdays // 2
    hour = 12 * (mdays % 2)
    time = aq.from_date(
        [
            np.ones(len(year)),
            year,
            month,
            day,
            hour,
        ]
    )
    return time
