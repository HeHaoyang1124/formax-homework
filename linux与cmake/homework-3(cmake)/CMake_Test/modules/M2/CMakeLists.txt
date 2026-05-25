add_library(M2 src/M2.cpp)

target_include_directories(M2 PUBLIC include)

target_link_libraries(M2 PUBLIC A1 A2 kalman)

