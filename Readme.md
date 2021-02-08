# VSCode Dotfiles

## Installation

1. Download [vscode](https://code.visualstudio.com/Download)
2. Open the user folder
   - Windows: `%appdata%/code/user`
   - Linux: `$HOME/.config/code/user`
3. Sync to the github account
4. Clone Settings from git repo

    ```sh
    git init
    git remote add origin https://github.com/incoggnito/vscode-settings.git
    git branch -M main
    git push -u origin main
    ```
