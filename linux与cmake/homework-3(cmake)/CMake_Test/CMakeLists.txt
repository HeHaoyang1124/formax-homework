cmake_minimum_required(VERSION 3.10)
project(Test)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 第三方依赖
find_package(OpenCV REQUIRED)

# 添加子目录
add_subdirectory(common)
add_subdirectory(modules)

# 生成可执行文件
add_executable(test main.cpp)

target_link_libraries(test PRIVATE
        M1
        M2
        Math
        ${OpenCV_LIBS}
)