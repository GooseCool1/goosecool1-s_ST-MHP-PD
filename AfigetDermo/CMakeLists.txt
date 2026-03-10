cmake_minimum_required(VERSION 4.1)
project(AfigetDermo)

set(CMAKE_CXX_STANDARD 20)

include_directories(/usr/include/x86_64-linux-gnu)

add_executable(AfigetDermo main.cpp !includes.h)