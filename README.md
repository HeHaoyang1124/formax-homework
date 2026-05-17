# 2026 SCUT Racing招新Linux&Catia&cmake作业

## Linux

1. 在当前目录下创建一个名为 linux_practice的文件夹，其内部包含两个子目录：docs 和 backup。
2. 在 docs 目录下创建三个文件：readme.txt、notes.log 和 temp.tmp。
3. 删除 temp.tmp 文件，将 notes.log 重命名为 daily_report.txt
4. 向 daily_report.txt 写入第一行内容：“Project Status: Active”
   追加第二行内容，显示当前系统日期（使用 date 命令）
5. 将 docs 目录下的所有 .txt 文件复制到 backup 目录下。
6. 将 backup 目录下所有文件的权限修改为 只读 -r--r--r—

最终输出结果

``` plaintext
Archive Complete. File [./backup/readme.txt] is now read-only
Archive Complete. File [./backup/daily_report.txt] is now read-only
```

## CMake

1. 代码思路
    1. 查看 main.cpp，根据 include 信息递归序查看依赖关系
        - `common` 依赖 `OpenCV`
        - `modules`
            - `A1`, `A2` 无外部依赖
            - `M1` 依赖 `A1`
            - `M2` 依赖 `A1`, `A2`, `common/kalman`
        - `main` 依赖 `modules`, `common`, `OpenCV`
    2. 根据依赖关系确定 `include` 路径
    3. 子目录 `modules` 生成同名静态库，并链接 `opencv`（`因为common需要`）
    4. 主程序 `main` 生成可执行文件，并链接 `modules` 和 `opencv`

2. 遇到问题： **CMake_I** 中，`./common/CMakeLists.txt` 会遍历设置所有子级文件夹为 **sub-directory**，
而 `./common/math/` 缺失 `CMakeLists.txt` 文件，导致错误

3. 解决思路：添加 `./common/math/CMakeLists.txt` 文件，
并追加 `math/include/` 路径到 `Common_INCLUDE_DIRS` 供父级 `main.cpp` 使用