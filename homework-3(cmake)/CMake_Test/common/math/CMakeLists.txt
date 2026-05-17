add_library(Math ${CMAKE_CURRENT_LIST_DIR}/src/Math.cpp)

target_include_directories(Math
        PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/include
        ${OpenCV_INCLUDE_DIRS}
)

target_link_libraries(Math PUBLIC ${OpenCV_LIBS})
