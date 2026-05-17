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
