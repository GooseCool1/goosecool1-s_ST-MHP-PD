cmake_minimum_required(VERSION 3.16)
project(ProtoOnYourScreen)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui)

add_executable(ProtoOnYourScreen
        src/main.cpp
)

target_link_libraries(ProtoOnYourScreen
        Qt6::Core
        Qt6::Widgets
        Qt6::Gui
)