add_library(M2 ${CMAKE_CURRENT_LIST_DIR}/src/M2.cpp)

target_include_directories(M2 PUBLIC ${CMAKE_CURRENT_LIST_DIR}/include)

target_link_libraries(M2 PUBLIC A1 A2 kalman)

