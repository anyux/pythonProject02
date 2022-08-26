#!/usr/bin/env python
function compileOpenssl() {
  #编译安装openssl库
  rm -rf /usr/local/openssl
  mkdir -p /usr/local/openssl
  cd /usr/local/openssl
  wget https://www.openssl.org/source/openssl-1.1.1a.tar.gz

  tar -zxvf openssl-1.1.1a.tar.gz

  cd openssl-1.1.1a
  ./config --prefix=/usr/local/openssl no-zlib #不需要zlib
  make
  make install

  mv /usr/bin/openssl /usr/bin/openssl.bak
  mv /usr/include/openssl/ /usr/include/openssl.bak

  ln -s /usr/local/openssl/include/openssl /usr/include/openssl
  ln -s /usr/local/openssl/lib/libssl.so.1.1 /usr/local/lib64/libssl.so
  ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl

  echo "/usr/local/openssl/lib" >>/etc/ld.so.conf
  ldconfig -v
}

function compilePython() {
  version=$1
  #编译安装python
  rm -rf /tmp/Python*.tar.xz
  cd /tmp
  wget https://registry.npmmirror.com/-/binary/python/${version}/Python-${version}.tar.xz
  tar xvf Python-${version}.tar.xz
  cd Python-${version}
  ./configure --prefix=/usr/local/python3 --with-openssl=/usr/local/openssl
  make
  make install
  echo export PATH=/usr/local/python3/bin:\$PATH >>/etc/profile

}

function main() {
  compileOpenssl
  compilePython $1
}

main $1
