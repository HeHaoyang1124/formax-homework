# 1
mkdir linux_practice
cd linux_practice

mkdir docs
mkdir backup

# 2
cd docs
touch readme.txt
touch notes.log
touch temp.tmp

# 3
rm temp.tmp
mv notes.log daily_report.txt

# 4
echo "Project Status: Active" > daily_report.txt
date >> daily_report.txt

# 5
cd ..
cp -r ./docs/*.txt ./backup

# 6
find ./backup/ -type f -exec chmod 444 {} \;
find ./backup/ -type f -exec echo "Archive Complete. File [{}] is now read-only" \;
