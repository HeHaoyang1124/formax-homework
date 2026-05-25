file(GLOB A1_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_library(
        A1
        src/A11.cpp
        src/A12.cpp
        src/A13.cpp
)

target_include_directories(A1 PUBLIC include)

