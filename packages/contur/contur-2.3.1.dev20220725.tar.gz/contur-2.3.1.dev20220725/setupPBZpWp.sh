#!/bin/bash

compiler_install_dir=/unix/cedar/altakach/compilers
export LD_LIBRARY_PATH=$compiler_install_dir/gcc/6.5.0/lib64:$compiler_install_dir/gmp/4.3.2/lib:$compiler_install_dir/mpfr/2.4.2/lib:$compiler_install_dir/mpc/0.8.1/lib:$compiler_install_dir/isl/0.15/lib:$LD_LIBRARY_PATH
install_dir=/unix/cedar/altakach/tools
export LD_LIBRARY_PATH=$install_dir/recola2-collier-2.2.1/recola2-2.2.1/:$LD_LIBRARY_PATH
