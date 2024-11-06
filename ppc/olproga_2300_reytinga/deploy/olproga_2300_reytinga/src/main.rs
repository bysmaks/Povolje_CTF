use core::panic;
use gcd::Gcd;
use prime_factorization::Factorization;
use std::{
    collections::HashMap,
    env,
    io::{Read, Write},
    net::{TcpListener, TcpStream},
    sync::Arc,
    time::SystemTime,
};
use threadpool::ThreadPool;

fn run_interp(
    fractions: Vec<(Vec<u64>, Vec<u64>)>,
    initial_value: u64,
) -> Result<HashMap<u64, u64>, String> {
    let start = SystemTime::now();
    let mut num_inst = 0;
    let factors = Factorization::run(initial_value).factors;
    let mut num = HashMap::new();
    for i in factors {
        num.entry(i).and_modify(|n| *n += 1).or_insert(1);
    }
    loop {
        let mut flag = false;
        for (n, d) in &fractions {
            let mut test = num.clone();
            let mut can_exec = true;
            for i in d {
                match test.get_mut(i) {
                    None => {
                        can_exec = false;
                        break;
                    }
                    Some(q) => {
                        if *q == 0 {
                            can_exec = false;
                            break;
                        } else {
                            *q -= 1
                        }
                    }
                }
            }
            drop(test);
            if can_exec {
                flag = true;
                num_inst += 1;
                for i in d {
                    num.entry(*i).and_modify(|x| *x -= 1);
                }
                for i in n {
                    num.entry(*i).and_modify(|x| *x += 1).or_insert(1);
                }
                if num_inst % 500 == 0 {
                    if start
                        .elapsed()
                        .map_err(|_| "Could not get time")?
                        .as_millis()
                        >= 500
                    {
                        return Err("Hit TL!".to_owned());
                    }
                }

                break;
            }
        }
        if !flag {
            for (k, v) in &num.clone() {
                if *v == 0 {
                    num.remove(k);
                }
            }
            return Ok(num);
        }
    }
}

static MAX_INSTRUCTIONS: usize = 100;
fn check(fractions: &Vec<(u64, u64)>) -> Result<Vec<(Vec<u64>, Vec<u64>)>, &str> {
    if fractions.len() > MAX_INSTRUCTIONS {
        return Err("Too many instructions!");
    }
    let mut res = Vec::new();
    for (n, d) in fractions {
        if *d == 0 {
            return Err("Denominator can't be 0!");
        }
        if n.gcd(*d) != 1 {
            return Err("Numerator and denominator must be relatively prime!");
        }
        let f_n = Factorization::run(*n);
        let f_d = Factorization::run(*d);
        res.push((f_n.factors, f_d.factors));
    }
    Ok(res)
}

fn run(program: &str, initial_value: u64) -> Result<HashMap<u64, u64>, String> {
    let mut fractions: Vec<(u64, u64)> = Vec::new();
    for f in program.trim().split(" ") {
        let nd = f
            .trim()
            .split_once("/")
            .ok_or("Fractions must be in form of a/b!".to_string())?;
        let n =
            nd.0.parse()
                .map_err(|x| format!("Could not parse a number: {x}"))?;
        let d =
            nd.1.parse()
                .map_err(|x| format!("Could not parse a number: {x}"))?;
        fractions.push((n, d));
    }
    Ok(run_interp(check(&fractions)?, initial_value)?)
}

fn client_handler(mut stream: TcpStream, flag: String) {
    let mut read = [0; 4096];
    stream
        .write(
            r#"
Hi there! Give me a list of fractions that will return 3^(n^2) with an input of 2^n.
The program is in the form of a/b c/d e/f..., no more that 100 fractions.
TL is 0.5 seconds for all tests, the program will be tested for number from 1 to 60.
Good luck!
Program: "#
                .as_bytes(),
        )
        .unwrap();
    match stream.read(&mut read) {
        Ok(_) => {
            let program = String::from_utf8(read.to_vec()).unwrap();
            let mut correct = true;
            for n in 1..61u32 {
                let r = run(&program.trim_end_matches('\x00'), 2u64.pow(n));
                match r {
                    Ok(num) => {
                        if *num.get(&3).unwrap_or(&70) == (n * n) as u64 {
                            stream.write(format!("[{n}/60] Ok!\n").as_bytes()).unwrap();
                        } else {
                            stream
                                .write(
                                    format!("[{n}/60] Failed: `Wrong answer on input {n}`\n")
                                        .as_bytes(),
                                )
                                .unwrap();
                            correct = false;
                        }
                    }
                    Err(e) => {
                        stream
                            .write(format!("[{n}/60] Failed: `{e}`\n").as_bytes())
                            .unwrap();
                        stream
                            .write(
                                format!("Skipping all further tests to not waste time\n")
                                    .as_bytes(),
                            )
                            .unwrap();
                        correct = false;
                        break;
                    }
                }
            }
            if correct {
                stream
                    .write(format!("Great job! Flag is {flag}\n").as_bytes())
                    .unwrap();
            }
        }
        Err(e) => panic!("{}", e),
    }
}

fn main() {
    let flag = env::var("FLAG").expect("Could not find flag in env variables!");
    let server = TcpListener::bind("0.0.0.0:8888").expect("Could not start TCP server!");
    let pool = Arc::new(ThreadPool::new(10));
    println!("Serving on port 8888...");
    for stream in server.incoming() {
        let f = flag.clone();
        match stream {
            Ok(s) => {
                eprintln!("[SRV] New connection!");
                pool.execute(move || client_handler(s, f))
            }
            Err(_) => eprintln!("[SRV] Stream error"),
        }
    }
}
