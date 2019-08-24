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


def check(toolchain, features):
    for subset in powerset(features):
        feature_str = ",".join(subset)
        print("$ cargo +" + toolchain + " check --features " + feature_str)

        status = subprocess.run([
            "cargo", "+" + toolchain, "check", "--features", feature_str
        ])
        if status.returncode != 0:
            sys.exit(1)


features = [
    "alloc",
    "std",
    # "unstable",
    "compat_hash",
    "compat_macros",
]

check("stable", features)
check("nightly", features + ["unstable"])
