#!/usr/bin/env python3
"""Generate release-specific AUR and winget manifests from verified assets.

Usage: python3 scripts/package-manifests.py v4.1.0 dist packaging-out
The input directory must contain checksums.txt and the Linux/Windows archives.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile
import zipfile


def generate(tag, assets, output):
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("package manifests require a stable vX.Y.Z tag")
    version = tag[1:]
    sums = {}
    for line in (assets / "checksums.txt").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        sums[name.lstrip("*")] = digest

    def checksum(name):
        digest = hashlib.sha256((assets / name).read_bytes()).hexdigest()
        if sums.get(name) != digest:
            raise ValueError(f"checksum mismatch or missing checksum: {name}")
        return digest

    linux = "utuimp_linux_amd64.tar.gz"
    windows = "utuimp_windows_amd64.zip"
    linux_sha, windows_sha = checksum(linux), checksum(windows)
    base = f"https://github.com/tphx37/utuimp/releases/download/{tag}"
    aur = output / "aur" / "utuimp-bin"
    aur.mkdir(parents=True, exist_ok=True)
    (aur / "PKGBUILD").write_text(f'''# Maintainer: tphx37 <https://github.com/tphx37>
pkgname=utuimp-bin
pkgver={version}
pkgrel=1
pkgdesc='Universal terminal user interface media player'
arch=('x86_64')
url='https://github.com/tphx37/utuimp'
license=('GPL-3.0-or-later' 'MIT')
depends=('glibc' 'gstreamer' 'gst-plugins-base' 'gst-plugins-good' 'gst-libav' 'fontconfig')
optdepends=('yt-dlp: YouTube Music and SoundCloud' 'ffmpeg: YouTube Music and SoundCloud' 'librespot: Spotify Premium')
provides=('utuimp')
conflicts=('utuimp' 'utuimp-git')
source=("utuimp-$pkgver.tar.gz::{base}/{linux}")
sha256sums=('{linux_sha}')

package() {{
  install -Dm755 "$srcdir/utuimp" "$pkgdir/usr/bin/utuimp"
  install -Dm644 "$srcdir/flatpak/io.github.tphx37.utuimp.desktop" "$pkgdir/usr/share/applications/io.github.tphx37.utuimp.desktop"
  install -Dm644 "$srcdir/assets/logo.png" "$pkgdir/usr/share/icons/hicolor/256x256/apps/io.github.tphx37.utuimp.png"
  install -Dm644 "$srcdir/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 "$srcdir/NOTICE" "$pkgdir/usr/share/licenses/$pkgname/NOTICE"
}}
''')
    # Three manifests can be submitted directly to microsoft/winget-pkgs.
    winget = output / "winget" / "manifests" / "t" / "tphx37" / "utuimp" / version
    winget.mkdir(parents=True, exist_ok=True)
    common = {"PackageIdentifier": "tphx37.utuimp", "PackageVersion": version, "ManifestVersion": "1.9.0"}
    manifests = {
        "": dict(common, DefaultLocale="en-US", ManifestType="version"),
        ".installer": dict(common, InstallerType="zip", NestedInstallerType="portable",
            NestedInstallerFiles=[{"RelativeFilePath": "utuimp.exe", "PortableCommandAlias": "utuimp"}],
            UpgradeBehavior="uninstallPrevious", Commands=["utuimp"],
            Installers=[{"Architecture": "x64", "InstallerUrl": f"{base}/{windows}", "InstallerSha256": windows_sha.upper()}], ManifestType="installer"),
        ".locale.en-US": dict(common, PackageLocale="en-US", Publisher="tphx37", PackageName="utuimp",
            PackageUrl="https://github.com/tphx37/utuimp", License="GPL-3.0-or-later",
            LicenseUrl="https://github.com/tphx37/utuimp/blob/main/LICENSE",
            ShortDescription="Universal terminal user interface media player", ManifestType="defaultLocale"),
    }
    for suffix, value in manifests.items():
        # JSON is valid YAML; winget consumes these .yaml files directly.
        header = ("# yaml-language-server: $schema=https://aka.ms/winget-manifest."
                  f"{value['ManifestType']}.{value['ManifestVersion']}.schema.json\n\n")
        (winget / f"tphx37.utuimp{suffix}.yaml").write_text(header + json.dumps(value, indent=2) + "\n")
    metadata = [
        "pkgbase = utuimp-bin", "\tpkgdesc = Universal terminal user interface media player",
        f"\tpkgver = {version}", "\tpkgrel = 1", "\turl = https://github.com/tphx37/utuimp",
        "\tarch = x86_64", "\tlicense = GPL-3.0-or-later", "\tlicense = MIT",
    ]
    metadata += [f"\tdepends = {name}" for name in ("glibc", "gstreamer", "gst-plugins-base", "gst-plugins-good", "gst-libav", "fontconfig")]
    metadata += [f"\toptdepends = {value}" for value in ("yt-dlp: YouTube Music and SoundCloud", "ffmpeg: YouTube Music and SoundCloud", "librespot: Spotify Premium")]
    metadata += ["\tprovides = utuimp", "\tconflicts = utuimp", "\tconflicts = utuimp-git",
        f"\tsource = utuimp-{version}.tar.gz::{base}/{linux}", f"\tsha256sums = {linux_sha}", "", "pkgname = utuimp-bin", ""]
    (aur / ".SRCINFO").write_text("\n".join(metadata))
    # Package metadata only; the source archives are never extracted here.
    (output / "packaging.tar.gz").parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output / "packaging.tar.gz", "w:gz") as archive:
        archive.add(aur.parent, arcname="aur")
        archive.add(output / "winget", arcname="winget")

    with zipfile.ZipFile(output / "packaging.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for root in (aur.parent, output / "winget"):
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("assets", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    generate(args.tag, args.assets, args.output)
