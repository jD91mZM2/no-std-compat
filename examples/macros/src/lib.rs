#![cfg_attr(not(feature = "std"), no_std)]

extern crate no_std_compat as std;

// Normally, putting this behind a feature gate is not needed to avoid
// unused_imports warnings. This time, it is. This is simply because
// in the normal Rust std, the standard macros are technically not in
// the prelude.
#[cfg(not(feature = "std"))]
use std::prelude::v1::*;

pub fn greet(who: &str) {
    if dbg!(who.trim()).is_empty() {
        eprintln!("Can't greet empty string!");
        eprintln!();
        eprint!(":|")
    }
    println!("Hello, {}.", who);
    print!("Nice to meet you!");
    println!();
}
