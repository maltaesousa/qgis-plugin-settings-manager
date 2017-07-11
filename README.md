Settings Manager
================

This is a fork from [sitnyon/qgis-plugin-settings-manager](https://github.com/sitnyon/qgis-plugin-settings-manager)
**Settings Manager** is a QGIS plugin to set default settings, specific for **Ville d'Yverdon-les-Bains** users.

Installation
------------

### Windows

Copy the folder `SettingsManager` into `%USERPROFILE%\.qgis2\python\plugins`.
> The files `Makefile`, `resources.qrc` and `ui_settingsmanager.ui` are not necessary.

Copy the file `DefaultProject/project_default.qgs` into `%USERPROFILE%\.qgis2`.

### Linux
Build the plugin with _make_:

```bash
make deploy
```
