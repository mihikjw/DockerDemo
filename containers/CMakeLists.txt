cmake_minimum_required(VERSION 3.10.2)
project(container_demo)
set(CMAKE_C_FLAGS "-std=c99")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
file(GLOB SOURCES
    *.c
)
add_executable(container_demo "${SOURCES}")