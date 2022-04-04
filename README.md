# Secrets
App to encrypt/decrypt secrets using the `AES-256-CBC` cipher.

---

## Anaconda Setup:
- conda create --name secrets python=3.9
```
The following packages will be downloaded:

package                    |            build
---------------------------|-----------------
ca-certificates-2022.3.29  |       h06a4308_0         117 KB
openssl-1.1.1n             |       h7f8727e_0         2.5 MB
python-3.9.11              |       h12debd9_2        19.2 MB
sqlite-3.38.2              |       hc218d9a_0         1.0 MB
tzdata-2022a               |       hda174b7_0         109 KB
------------------------------------------------------------
Total:        22.9 MB

The following NEW packages will be INSTALLED:

_libgcc_mutex      pkgs/main/linux-64::_libgcc_mutex-0.1-main
_openmp_mutex      pkgs/main/linux-64::_openmp_mutex-4.5-1_gnu
ca-certificates    pkgs/main/linux-64::ca-certificates-2022.3.29-h06a4308_0
certifi            pkgs/main/linux-64::certifi-2021.10.8-py39h06a4308_2
ld_impl_linux-64   pkgs/main/linux-64::ld_impl_linux-64-2.35.1-h7274673_9
libffi             pkgs/main/linux-64::libffi-3.3-he6710b0_2
libgcc-ng          pkgs/main/linux-64::libgcc-ng-9.3.0-h5101ec6_17
libgomp            pkgs/main/linux-64::libgomp-9.3.0-h5101ec6_17
libstdcxx-ng       pkgs/main/linux-64::libstdcxx-ng-9.3.0-hd4cf53a_17
ncurses            pkgs/main/linux-64::ncurses-6.3-h7f8727e_2
openssl            pkgs/main/linux-64::openssl-1.1.1n-h7f8727e_0
pip                pkgs/main/linux-64::pip-21.2.4-py39h06a4308_0
python             pkgs/main/linux-64::python-3.9.11-h12debd9_2
readline           pkgs/main/linux-64::readline-8.1.2-h7f8727e_1
setuptools         pkgs/main/linux-64::setuptools-58.0.4-py39h06a4308_0
sqlite             pkgs/main/linux-64::sqlite-3.38.2-hc218d9a_0
tk                 pkgs/main/linux-64::tk-8.6.11-h1ccaba5_0
tzdata             pkgs/main/noarch::tzdata-2022a-hda174b7_0
wheel              pkgs/main/noarch::wheel-0.37.1-pyhd3eb1b0_0
xz                 pkgs/main/linux-64::xz-5.2.5-h7b6447c_0
zlib               pkgs/main/linux-64::zlib-1.2.11-h7f8727e_4
```

- conda activate secrets

- conda install pycryptodome
```
The following packages will be downloaded:

package                    |            build
---------------------------|-----------------
pycryptodome-3.12.0        |   py39hdd9d17f_0         1.3 MB
------------------------------------------------------------
Total:         1.3 MB

The following NEW packages will be INSTALLED:

gmp                pkgs/main/linux-64::gmp-6.2.1-h2531618_2
pycryptodome       pkgs/main/linux-64::pycryptodome-3.12.0-py39hdd9d17f_0
```

- conda install beautifulsoup4
```
The following packages will be downloaded:

package                    |            build
---------------------------|-----------------
soupsieve-2.3.1            |     pyhd3eb1b0_0          34 KB
------------------------------------------------------------
Total:          34 KB

The following NEW packages will be INSTALLED:

beautifulsoup4     pkgs/main/noarch::beautifulsoup4-4.10.0-pyh06a4308_0
soupsieve          pkgs/main/noarch::soupsieve-2.3.1-pyhd3eb1b0_0
```

