#!/bin/bash

# execute command
# -------------------
# curl -s https://raw.githubusercontent.com/karaage0703/vscode-dotfiles/master/install-vscode-extensions.sh | /bin/bash

# Visual Studio Code :: Package list
pkglist=(
alefragnani.project-manager
bierner.markdown-preview-github-styles
christian-kohler.path-intellisense
CoenraadS.bracket-pair-colorizer-2
Darfka.vbscript
DavidAnson.vscode-markdownlint
eamodio.gitlens
eightHundreds.vscode-drawio
esbenp.prettier-vscode
evilz.vscode-reveal
formulahendry.code-runner
Gruntfuggly.todo-tree
luggage66.VBScript
ms-python.python
ms-python.vscode-pylance
ms-toolsai.jupyter
njpwerner.autodocstring
redhat.vscode-yaml
samuelcolvin.jinjahtml
tomoyukim.vscode-mermaid-editor
vscode-icons-team.vscode-icons
vscodevim.vim
VSpaceCode.whichkey
yzhang.markdown-all-in-one
ZainChen.json
zhuangtongfa.material-theme
)

for i in ${pkglist[@]}; do
  code --install-extension $i
done