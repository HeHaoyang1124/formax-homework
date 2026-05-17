file(GLOB A1_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_library(
        A1
        ${CMAKE_CURRENT_LIST_DIR}/src/A11.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/A12.cpp
        ${CMAKE_CURRENT_LIST_DIR}/src/A13.cpp
)

target_include_directories(A1 PUBLIC ${CMAKE_CURRENT_LIST_DIR}/include)

