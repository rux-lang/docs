# Installation

This guide explains how to install the Rux compiler and package manager.

---

## Windows

### Scoop (Recommended)

Add the Rux Scoop bucket:

```powershell
scoop bucket add rux-lang https://github.com/rux-lang/Scoop
```

Install Rux:

```powershell
scoop install rux-lang/rux
```

### Releases

Prebuilt binaries are available from the GitHub releases page.

Available downloads:

* `.msi` — installs Rux on the system
* `.exe` — standalone Rux executable

The standalone executable can be used directly without running an installer.

---

## Arch Linux

Rux is available from the AUR.

```bash
yay -S rux-git
```

or

```bash
paru -S rux-git
```

---

## Fedora and COPR-Based Distributions

Enable the Rux COPR repository:

```bash
sudo dnf copr enable zapaxe/Rux-Lang
```

Install Rux:

```bash
sudo dnf install rux
```

---

## Other Distributions

For distributions without an official package, Rux can be built from source.

See the repository build instructions for the latest requirements and build steps.

---

## Verify Installation

Open a terminal and run:

```bash
rux version
```

Example output:

```text
Rux v0.3.0
```

The version number may differ depending on the installed release.

---

## Updating

### Scoop

```powershell
scoop update
scoop update rux
```

### Arch Linux

```bash
yay -Syu
```

### Fedora / COPR

```bash
sudo dnf upgrade
```
