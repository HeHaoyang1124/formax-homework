add_library(Math src/Math.cpp)

target_include_directories(Math
        PUBLIC
        include
        ${OpenCV_INCLUDE_DIRS}
)

target_link_libraries(Math PUBLIC ${OpenCV_LIBS})
