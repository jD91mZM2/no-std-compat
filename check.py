#!/usr/bin/env python3

import subprocess
import sys


def powerset(input):
    if len(input) == 0:
        return [[]]

    pivot = input[0]

    subset = powerset(input[1:])
    with_pivot = subset.copy()
    for i, set in enumerate(with_pivot):
        with_pivot[i] = [pivot] + set

    return subset + with_pivot


def execute(args, **kwargs):
    cwd = ""
    if "cwd" in kwargs:
        cwd += kwargs["cwd"] + "/ "
    print(cwd + "$ " + " ".join(args))
    status = subprocess.run(args, **kwargs)

    if status.returncode != 0:
        sys.exit(1)


def check(toolchain, features):
    for subset in powerset(features):
        feature_str = ",".join(subset)
        execute(["cargo", "+" + toolchain, "check", "--features", feature_str])


features = [
    "alloc",
    "std",
    # "unstable",
    "compat_hash",
    "compat_macros",
]

check("stable", features)
check("nightly", features + ["unstable"])

execute(["cargo", "test"], cwd="example-crates")
