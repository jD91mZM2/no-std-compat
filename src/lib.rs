#![cfg_attr(not(feature = "std"), no_std, feature(fixed_size_array, futures_api, core_intrinsics, core_panic_info, core_panic, raw, unicode_internals))]
#![cfg_attr(all(not(feature = "std"), feature = "alloc"), feature(alloc_prelude))]

#[cfg(all(not(feature = "std"), feature = "alloc"))]
extern crate alloc;

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
        let _ = format_args!($($arg)*);
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
    ($val:expr) => { $val }
}
