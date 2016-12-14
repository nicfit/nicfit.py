#!/bin/bash

TEST_D=./test_tmp
rm -rf $TEST_D
mkdir -p $TEST_D

cookiecutter -o $TEST_D . -f --no-input
