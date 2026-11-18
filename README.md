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
```

Remove:

```sh
sudo pacman -Rns utuimp
```

The repository becomes available when the first stable release with an
Arch package has been published. Current deployment:
[packages workflow](https://github.com/tphx37/utuimp-repo/actions/workflows/packages.yml).

## Homebrew (macOS and Linux x86_64)

The binary formula is published with the first supported stable release:

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

## Other packages

Versioned AUR recipes and winget manifests are stored in `aur/` and `winget/`
after each supported stable release. Availability through `yay` and the
winget community catalog depends on publication to their respective catalogs.

Removal preserves utuimp settings and your local music.
