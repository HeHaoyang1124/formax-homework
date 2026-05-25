file(GLOB M1_SOURCES CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)

add_library(M1 ${M1_SOURCES})

target_include_directories(M1
        PUBLIC
        include
)

target_link_libraries(M1
        PUBLIC
        A1
)

