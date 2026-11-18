#!/usr/bin/env python3
"""Write a binary Homebrew formula using verified release checksums."""
import hashlib
from pathlib import Path
import re
import sys

tag, asset_dir, destination = sys.argv[1:]
if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
    raise ValueError("expected stable version")
assets = Path(asset_dir)
sums = dict((name.lstrip("*"), digest) for digest, name in
            (line.split(maxsplit=1) for line in (assets / "checksums.txt").read_text().splitlines()))


def source(os, arch, indent):
    name = f"utuimp_{os}_{arch}.tar.gz"
    sha = hashlib.sha256((assets / name).read_bytes()).hexdigest()
    if sums.get(name) != sha:
        raise ValueError(f"checksum mismatch: {name}")
    return f'{indent}url "https://github.com/tphx37/utuimp/releases/download/{tag}/{name}"\n{indent}sha256 "{sha}"\n'


formula = '''class Utuimp < Formula
  desc "Universal terminal user interface media player"
  homepage "https://github.com/tphx37/utuimp"
  license "GPL-3.0-or-later"
'''
formula += f'  version "{tag[1:]}"\n'
formula += '  depends_on "fontconfig"\n\n  on_macos do\n    on_arm do\n'
formula += source("darwin", "arm64", "      ")
formula += '    end\n    on_intel do\n'
formula += source("darwin", "amd64", "      ")
formula += '    end\n  end\n\n  on_linux do\n    depends_on "gstreamer"\n    depends_on arch: :x86_64\n'
formula += source("linux", "amd64", "    ")
formula += '''  end

  def install
    bin.install "utuimp"
    prefix.install "NOTICE"
  end

  def caveats
    "For YouTube Music and SoundCloud: brew install yt-dlp ffmpeg\\nFor Spotify Premium: brew install librespot"
  end
end
'''
path = Path(destination)
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(formula)
