cd lib
ls | xargs -I{} bash -c 'cd {}; sed -n "/tool.poetry.dependencies/,/tool.poetry.dev/{//!p}" pyproject.toml' > packages
awk '!/atoolbox/' packages > tmp
awk '!/sqldb/' tmp > packages
awk '!/vaspy/' packages > tmp
awk '!/vallendb/' tmp > packages
awk '!/python/' packages > tmp
sort -u tmp >> unique
cat unique
rm packages unique tmp
cd ..
