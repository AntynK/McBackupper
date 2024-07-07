# Mc Backupper
Tool for making backups of Minecraft worlds from `saves` and `versions` folders.

## Installation
### Download .exe file
Download the archive [`McBackupper.windows.64.bit.zip`](https://github.com/AntynK/McBackupper/releases/latest), unpack it, and run the `.exe` file.

> [!IMPORTANT]  
> Antiviruses could mark this file as potentially malicious. You can try the second method.

### Download source code
Download the [`Source code(zip)`](https://github.com/AntynK/McBackupper/releases/latest) and unpack it.

The program was written in [Python 3.12.4](https://www.python.org/downloads/release/python-3124/) (versions up to 3.9 should also work) and the [flet](https://pypi.org/project/flet/0.23.1/) framework. It is better to download it from [requirements.txt](requirements.txt) using the command:

For Windows:
``` Bash
pip install -r requirements.txt
```

For Linux and macOS: 
``` Bash
pip3 install -r requirements.txt
```

Then run the [main.pyw](main.pyw) file using the command (or by double-clicking):

For Windows:
``` Bash
python main.pyw
```

For Linux and macOS: 
``` Bash
python3 main.pyw
```

## Basic
### Creation
All data that you have entered during creation are stored separately from the backup file.  
To change backup data, press and hold the left mouse button.

> [!NOTE]  
> Clicking the backup name will open it in the file explorer.

### Backup data
`File name` - the backup file name, by default is the world name. The creation date and `.zip` extension will be added after creation.
> [!NOTE]  
> This cannot be changed after creation.

`Title` - backup title, optional field.  
`Pool ignore` - when checked, the backup is not included in the pool.

### Backup pool
The pool (queue) automatically removes outdated backups.
By default, the pool is set to 4. This means if you have 4 backups (with the `Pool ignore` flag unchecked) and create a new backup, the oldest one will be deleted. 
> [!NOTE]  
> The program determines the oldest backup by the date that the user has entered.

### Restoring and deleting
When restoring, the world folder will be permanently deleted and replaced with the folder from the backup.
> [!IMPORTANT]  
> The program will immediately restore the world without popup windows.

When deleting, the backup file will be removed.
> [!IMPORTANT]  
> The program will immediately delete the backup without popup windows.

### Backup structure
All backups from the `saves` folder are saved at `<backups>/saves/<WorldName>/backups`. From the `versions` folder at `<backups>/versions/<VersionName>/saves/<WorldName>/backups`.

`<backups>` - the folder where all backups are saved (can be changed in settings).
`<VersionName>` - version name.  
`<WorldName>` - world name.  
`backups` - folder where world backups are saved.

> [!NOTE]  
> Names are taken from folder names, so they may be different from what you see in the game.

> [!TIP]  
> To get the name of the world folder, in select world menu you can look below the world name, or you can open it when editing the world.


## Features
The program can automatically determine the backup creation date (if it is formatted like `YEAR-MONTH-DAY_HOUR-MINUTE-SECOND`), so you can transfer backups created with Minecraft.

> [!NOTE]  
> Backups that have been transferred in this way will be included in the pool.

## Localizers
GNU gettext is used for localization. To add a new language, you need to create a subfolder with the [language code](https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html) (example `assets/locale/pl/LC_MESSAGES`).
Then copy template files(with `.pot` extension).
After filling in templete you can create [pull request](https://github.com/AntynK/McBackupper/pulls) (make sure to add `.mo` extension to `.gitignore`).

## Contributors
If you have ideas for improvement or want to contribute to the development of the project, please submit your contribution. See [CONTRIBUTING.md](CONTRIBUTING.md).
