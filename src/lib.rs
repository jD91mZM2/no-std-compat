#![cfg_attr(not(feature = "std"), no_std)]
#![cfg_attr(all(not(feature = "std"), feature = "unstable"),
            feature(core_intrinsics, core_panic_info, core_panic, raw, unicode_internals))]
#![cfg_attr(all(not(feature = "std"), feature = "alloc", feature = "unstable"),
            feature(alloc_prelude, raw_vec_internals))]

// The 2 underscores are used to avoid ambiguity (see
// https://gitlab.com/jD91mZM2/no-std-compat/issues/1)
#[cfg(all(not(feature = "std"), feature = "alloc"))]
extern crate alloc as __alloc;
extern crate core as __core;

#[cfg(not(feature = "std"))]
mod generated;

#[cfg(not(feature = "std"))]
pub use self::generated::*;
#[cfg(feature = "std")]
pub use std::*;

#[cfg(all(not(feature = "std"), feature = "compat_macros"))]
#[macro_export]
macro_rules! print {
    () => {{}};
    ($($arg:tt)+) => {{
        // Avoid unused arguments complaint. This surely must get
        // optimized away? TODO: Verify that
        let _ = format_args!($($arg)+);
    }};
}
#[cfg(all(not(feature = "std"), feature = "compat_macros"))]
#[macro_export]
macro_rules! println {
    ($($arg:tt)*) => { print!($($arg)*) }
}
#[cfg(all(not(feature = "std"), feature = "compat_macros"))]
#[macro_export]
macro_rules! eprint {
    ($($arg:tt)*) => { print!($($arg)*) }
}
#[cfg(all(not(feature = "std"), feature = "compat_macros"))]
#[macro_export]
macro_rules! eprintln {
    ($($arg:tt)*) => { print!($($arg)*) }
}

#[cfg(all(not(feature = "std"), feature = "compat_macros"))]
#[macro_export]
macro_rules! dbg {
    () => {};
    ($($val:expr),+) => { ($($val),+) }
}
