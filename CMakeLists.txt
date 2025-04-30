cmake_minimum_required(VERSION 3.11.0)

project(tribe VERSION 0.0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_PREFIX_PATH qt5application)

file(GLOB_RECURSE SRC_FILES data/*.cpp)
message(STATUS "SRC_FILES: " ${SRC_FILES})
message(STATUS "CMAKE_CURRENT_BINARY_DIR: " ${CMAKE_CURRENT_BINARY_DIR})
message(STATUS "CMAKE_CURRENT_SOURCE_DIR: " ${CMAKE_CURRENT_SOURCE_DIR})

find_package(Qt6 COMPONENTS Widgets REQUIRED)
find_package(SQLite3 REQUIRED)
find_package(Python REQUIRED)

include_directories(${SQLite3_INCLUDE_DIRS})

add_custom_command(
    OUTPUT  "${CMAKE_CURRENT_BINARY_DIR}/create_tables.sql"
    COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/data/generate_sql.py ${CMAKE_CURRENT_SOURCE_DIR}/data/db_models.hpp > "${CMAKE_CURRENT_BINARY_DIR}/create_tables.sql"
    DEPENDS data/generate_sql.py
    COMMENT "Generating SQL schema..."
)

add_custom_target(
    generate_sql ALL
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/data/db_models.hpp" "${CMAKE_CURRENT_BINARY_DIR}/create_tables.sql"
)

add_executable(tribe ${SRC_FILES} main.cpp)

target_link_libraries(tribe PRIVATE Qt6::Widgets)
target_link_libraries(tribe PRIVATE SQLite::SQLite3)
