cmake_minimum_required(VERSION 3.11.0)

project(tribe VERSION 0.0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_PREFIX_PATH qt5application)

find_package(Qt6 COMPONENTS Widgets REQUIRED)
find_package(SQLite3 REQUIRED)

file(GLOB_RECURSE SRC_FILES data/*.cpp)
message(STATUS "SRC_FILES: " ${SRC_FILES})

add_executable(tribe ${SRC_FILES} main.cpp)

include_directories(${SQLite3_INCLUDE_DIRS})

target_link_libraries(tribe PRIVATE Qt6::Widgets)
target_link_libraries(tribe PRIVATE SQLite::SQLite3)
