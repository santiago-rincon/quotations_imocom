# Quotations app

## Installation of requirements

It is necessary to install dependencies with `poetry` through the file `pyproject.toml`.

If you don't have poetry installed, you can install it with `pip`.
```
pip install poetry
```
Install dependencies from `pyproject.toml`:

```
poetry install
```
## Run in development mode
Installing through poetry creates a virtual environment, so it is no longer necessary to create one.

- Run as a desktop app:

```
poetry run flet run
```

- Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

## Installation via release
Download the `quotations.7z` file from the [releases page](https://github.com/santiago-rincon/quotations_imocom/releases). Unzip the file into a folder and place that folder in a path on your computer. Finally, run the `quotations.exe` file. The first time it will take a while to start up while the necessary files are created for it to work.

## Template editing
To edit the Word quotation template, you must access the following path:
- Windows: C:\Users\<your_user>\AppData\Roaming\Flet\quotations\flet\app\assets\shema.docx