## How it works
https://hackmd.io/Tlf08KuPTbqsHLKk5hzAvA

## Installation:

#### Tested in macOS High Sierra

1) Install python 3 and upgrade pip (requies [Homebrew](https://brew.sh/))
```
$ xcode-select --install (if needed)
$ brew install python3
$ brew install pkg-config autoconf automake libyaml
```

2) Clone Uniswap and Vyper repositories
```
$ git clone https://github.com/Uniswap/contracts-vyper
$ cd contracts-vyper
```

3) Setup virtual environment (recommended)
```
$ pip3 install --upgrade pip
$ pip3 install virtualenv
$ virtualenv uniswap_env
$ source uniswap_env/bin/activate
```

4) [Install Vyper](https://vyper.readthedocs.io/en/latest/installing-vyper.html)
```
$ brew install gmp
$ export CFLAGS="-I$(brew --prefix openssl)/include"
$ export LDFLAGS="-L$(brew --prefix openssl)/lib"
$ export CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix libyaml)/include"
$ export LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix libyaml)/lib"
$ pip install scrypt
$ git clone https://github.com/ethereum/vyper.git
$ cd vyper
$ make
$ make test
$ cd ..
```

5) Install other dependencies
```
$ pip install pytest
$ pip install ethereum
```

6) Run tests
```
$ cd tests
$ pytest -v
```