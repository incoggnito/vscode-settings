#!/bin/bash

# execute command
# -------------------
# curl -s https://raw.githubusercontent.com/karaage0703/vscode-dotfiles/master/install-vscode-extensions.sh | /bin/bash

# Visual Studio Code :: Package list
pkglist=(
ms-vscode.cpptools
ms-python.python
vscodevim.vim
donjayamanne.githistory
eamodio.gitlens
coenraads.bracket-pair-colorizer-2
vscode-icons-team.vscode-icons
github.github-vscode-theme
christian-kohler.path-intellisense
mhutchie.git-graph
Gruntfuggly.todo-tree
hediet.vscode-drawio
marp-team.marp-vscode
shd101wyy.markdown-preview-enhanced
shuworks.vscode-table-formatter
esbenp.prettier-vscode
davidanson.vscode-markdownlint
njpwerner.autodocstring
ms-python.vscode-pylance
alefragnani.project-manager
bierner.markdown-preview-github-styles
GrapeCity.gc-excelviewer
huntertran.auto-markdown-toc
mdickin.markdown-shortcuts
yzhang.markdown-all-in-one
)

for i in ${pkglist[@]}; do
  code --install-extension $i
done