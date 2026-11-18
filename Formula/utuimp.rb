class Utuimp < Formula
  desc "Universal terminal user interface media player"
  homepage "https://github.com/tphx37/utuimp"
  license "GPL-3.0-or-later"
  version "4.0.1"
  depends_on "fontconfig"

  on_macos do
    on_arm do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.1/utuimp_darwin_arm64.tar.gz"
      sha256 "fbc88a39c0791626e10755eef814f160704af31943166ee6bf655d1859e3c904"
    end
    on_intel do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.1/utuimp_darwin_amd64.tar.gz"
      sha256 "e5893b70ca17fda072fafcd330a85dd696d1ca896d26841bf5380d64a0f4caac"
    end
  end

  on_linux do
    depends_on "gstreamer"
    depends_on arch: :x86_64
    url "https://github.com/tphx37/utuimp/releases/download/v4.0.1/utuimp_linux_amd64.tar.gz"
    sha256 "aaef0b284ab0d614872c3d846450fe367f2b6e1e9ae6683b5254bae3e97293ff"
  end

  def install
    bin.install "utuimp"
    prefix.install "NOTICE"
  end

  def caveats
    "For YouTube Music and SoundCloud: brew install yt-dlp ffmpeg\nFor Spotify Premium: brew install librespot"
  end
end
