#!/usr/bin/env python3

from collections import namedtuple
from dataclasses import dataclass, field
import argparse
import os
import re
import subprocess
import sys

Namespace = namedtuple("Namespace", "name module")

@dataclass
class Module:
    unstable: bool
    cfgs: list = field(default_factory=list)

# Parse arguments

parser = argparse.ArgumentParser(
    description="Generate a std compatibility module"
)
parser.add_argument("--src", help=(
    "Specify the location of the rust source code. The default is "
    "`$(rustc --print sysroot)/lib/rustlib/src/rust/library`"
))
args = parser.parse_args()

if args.src is None:
    output = subprocess.run(["rustc", "--print", "sysroot"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    args.src = os.path.join(output.stdout.decode("utf-8").strip(),
                            "lib", "rustlib", "src", "rust", "library")


# Read files

modules_regex = re.compile(
    r"^(?:\S.*)?pub\s+(?:mod\s+|use\s+(?:[a-zA-Z_][a-zA-Z0-9_]*::)*)"
    r"([a-zA-Z_][a-zA-Z0-9_]*);",
    re.MULTILINE
)


def modules(crate):
    """
    Return a dictionary of all modules and whether they appear unstable or not.
    """
    root = os.path.join(args.src, crate, "src")
    lib = os.path.join(root, "lib.rs")
    with open(lib) as f:
        contents = f.read()

    modules = dict()
    for match in modules_regex.finditer(contents):
        module = match.group(1)
        unstable = False

        path = os.path.join(root, module + ".rs")
        if not os.path.isfile(path):
            path = os.path.join(root, module, "mod.rs")
        try:
            with open(path, "r") as f:
                unstable = "#![unstable" in f.read()
                if unstable:
                    print(
                        f"Module '{module}' from '{crate}' appears unstable",
                        file=sys.stderr
                    )
        except OSError as e:
            print(e, file=sys.stderr)
            pass

        modules[module] = Module(unstable)
    return modules


def generate(module, *namespaces):
    """
    Generate code for any module, given its name and which namespaces it appears
    under and whether it's unstable or not.
    """
    out = f"pub mod {module} {{\n"

    if module == "prelude":
        return None

    for namespace in namespaces:
        out += "    "

        cfgs = []
        if namespace.name != "core":
            cfgs.append(f"feature = \"{namespace.name}\"")
        if namespace.module.unstable:
            cfgs.append("feature = \"unstable\"")
        cfgs += namespace.module.cfgs

        if len(cfgs) == 1:
            out += f"#[cfg({cfgs[0]})] "
        elif len(cfgs) > 1:
            out += "#[cfg(all(" + ", ".join(cfgs) + "))] "

        out += f"pub use __{namespace.name}::{module}::*;\n"

    if module == "collections":
        prefix = (
            "    #[cfg(all("
            "feature = \"alloc\", "
            "feature = \"compat_hash\""
            "))] pub use hashbrown::"
        )
        out += (
            prefix + "HashMap;\n" +
            prefix + "HashSet;\n"
        )
    elif module == "sync":
        prefix = (
            "    #[cfg(all("
            "feature = \"alloc\", "
            "feature = \"compat_sync\""
            "))] pub use spin::"
        )
        out += (
            prefix + "Mutex;\n" +
            prefix + "MutexGuard;\n" +
            prefix + "Once;\n" +
            prefix + "RwLock;\n" +
            prefix + "RwLockReadGuard;\n" +
            prefix + "RwLockWriteGuard;\n"
        )

    out += "}"
    return out


# Main logic

core = modules("core")
alloc = modules("alloc")

# Module overrides
core["lazy"].unstable = True
alloc["sync"].cfgs.append("not(target_os = \"none\")")
alloc["task"].cfgs.append("not(target_os = \"none\")")

generated = {}

core_keys = set(core.keys())
alloc_keys = set(alloc.keys())

# Appearing in both
for module in core_keys & alloc_keys:
    generated[module] = generate(
        module,
        Namespace("core", core[module]),
        Namespace("alloc", alloc[module]),
    )

# Only in core
for module in core_keys - alloc_keys:
    generated[module] = generate(
        module,
        Namespace("core", core[module]),
    )

# Only in alloc
for module in alloc_keys - core_keys:
    generated[module] = generate(
        module,
        Namespace("alloc", alloc[module]),
    )

# Complete module overrides

generated["prelude"] = """pub mod prelude {
    pub mod v1 {
        // Prelude
        pub use __core::prelude::v1::*;
        #[cfg(all(feature = "alloc", feature = "unstable"))]
        pub use __alloc::prelude::v1::*;
        #[cfg(all(feature = "alloc", not(feature = "unstable")))]
        pub use __alloc::{
            borrow::ToOwned,
            boxed::Box,
            // UNSTABLE: slice::SliceConcatExt,
            string::String,
            string::ToString,
            vec::Vec,
        };

        // Other imports
        #[cfg(feature = "alloc")]
        pub use __alloc::{format, vec};
        #[cfg(feature = "compat_macros")]
        pub use crate::{print, println, eprint, eprintln, dbg};
    }
}"""

print("""//! Generated by generate.py located at the repository root
//! ./generate.py > src/generated.rs""")
for module in sorted(generated.items(), key=lambda i: i[0]):
    print(module[1])
