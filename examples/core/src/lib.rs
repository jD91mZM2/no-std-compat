#![cfg_attr(not(feature = "std"), no_std)]

extern crate no_std_compat as std;

// use std::prelude::v1::*;

// ^ Not needed when only using core; Rust inserts
// ```rust
// use core::prelude::v1::*
// ```
// by default...

use std::{
    num::NonZeroUsize,
    sync::atomic::{AtomicUsize, Ordering}
};

static CONST: AtomicUsize = AtomicUsize::new(0);

pub fn bump_counter() {
    CONST.fetch_add(1, Ordering::SeqCst);
}
pub fn get_counter() -> usize {
    CONST.load(Ordering::SeqCst)
}
pub fn get_counter_nonzero() -> Option<NonZeroUsize> {
    NonZeroUsize::new(get_counter())
}
