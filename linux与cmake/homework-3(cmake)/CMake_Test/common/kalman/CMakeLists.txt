find_package(OpenCV REQUIRED)

add_library(kalman INTERFACE)

target_include_directories(kalman
        INTERFACE
        include
        ${OpenCV_INCLUDE_DIRS}
)
