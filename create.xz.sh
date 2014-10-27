#!/bin/bash
version="`cat setup.spec | grep Version: | awk '{print $2}'`"
git clone https://abf.io/omv_software/setup.git setup-$version
rm -rf setup-$version/.git
tar cfJ setup-$version.tar.xz setup-$version
