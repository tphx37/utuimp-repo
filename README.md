# utuimp packages

Packages for [utuimp](https://github.com/tphx37/utuimp).
The catalog follows stable releases automatically.

## Arch Linux (x86_64)

Import the repository key and verify its fingerprint:

```sh
curl -fsSLo /tmp/utuimp-repo.asc https://raw.githubusercontent.com/tphx37/utuimp-repo/main/utuimp-repo.asc
gpg --show-keys --with-fingerprint /tmp/utuimp-repo.asc
```

Expected fingerprint: `60F4 201F 00C8 8341 B129 EFF6 E2B2 3C22 E366 E8CD`.

```sh
sudo pacman-key --add /tmp/utuimp-repo.asc
sudo pacman-key --lsign-key 60F4201F00C88341B129EFF6E2B23C22E366E8CD
```

Add the following to `/etc/pacman.conf`:

```ini
[utuimp]
SigLevel = Required DatabaseRequired
Server = https://tphx37.github.io/utuimp-repo/$arch
```

Install or update:

```sh
sudo pacman -Syu utuimp
# Or, with yay / paru after the same repository setup:
yay -Syu utuimp
```

Remove:

```sh
sudo pacman -Rns utuimp
# Or:
yay -Rns utuimp
```

Packages and the database are signed. New stable releases are published automatically.
[Deployment status](https://github.com/tphx37/utuimp-repo/actions/workflows/packages.yml).

## Homebrew (macOS and Linux x86_64)

Install a release binary:

```sh
brew tap --custom-remote tphx37/utuimp-repo https://github.com/tphx37/utuimp-repo.git
brew install tphx37/utuimp-repo/utuimp
brew upgrade tphx37/utuimp-repo/utuimp
```

Remove:

```sh
brew uninstall utuimp
brew untap tphx37/utuimp-repo
```

## AUR

Versioned recipes are available in `aur/`. They have not yet been published
to the AUR catalog. `yay -Syu utuimp` already works through the signed
repository configured above.

## Windows / winget

[Community catalog submission](https://github.com/microsoft/winget-pkgs/pull/483188)
is pending. Until accepted, install the published local manifest in PowerShell
(enable local manifests in an administrator terminal):

```powershell
winget settings --enable LocalManifestFiles
Invoke-WebRequest https://github.com/tphx37/utuimp/releases/latest/download/packaging.zip -OutFile packaging.zip
Expand-Archive .\packaging.zip -DestinationPath .\utuimp-packaging -Force
$manifest = Get-ChildItem .\utuimp-packaging\winget\manifests\t\tphx37\utuimp -Directory | Sort-Object Name -Descending | Select-Object -First 1
winget install --manifest $manifest.FullName
```

After catalog acceptance:

```powershell
winget install --id tphx37.utuimp --exact
```

Remove either installation:

```powershell
winget uninstall --id tphx37.utuimp --exact
```

Removal preserves utuimp settings and your local music.
