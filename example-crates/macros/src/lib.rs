#![no_std]

extern crate no_std_compat as std;

use std::prelude::v1::*;

pub fn greet(who: &str) {
    if dbg!(who.trim()).is_empty() {
        eprintln!("Can't greet empty string!");
        eprintln!();
        eprint!(":|")
    }
    println!("Hello, {}.", who);
    let (meet, you) = dbg!("meet", "you");
    print!("Nice to {} {}!", meet, you);
    println!();
}
