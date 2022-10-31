# VSCode Dotfiles

## Installation

1. Download vscode https://code.visualstudio.com/Download
2. Open the user folder `%appdata%/code/user`
3. Clone Settings from git repo

```sh
git init
git remote add origin https://github.com/incoggnito/vscode-settings
git pull origin main
```

Update the extensions File

```powershell
code --list-extensions | Out-File -FilePath  $env:appdata\Code\User\extensions.vsix
```

4. Run `extensions.sh`
