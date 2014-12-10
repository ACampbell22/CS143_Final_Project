#!/usr/bin/env sh

case $1 in
    "test")
        echo "==== Testing file_ecc.py ===="
        python file_ecc.py
        echo "==== Testing rs_code.py ===="
        python rs_code.py
        echo "==== Testing genericmatrix.py ===="
        python genericmatrix.py
        echo "==== Testing ffield.py ===="
        python ffield.py
        ;;
    "clean")
        rm *.lut.*
        ;;
    *)
        echo "Invalid argument"
        ;;
esac

