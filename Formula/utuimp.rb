class Utuimp < Formula
  desc "Universal terminal user interface media player"
  homepage "https://github.com/tphx37/utuimp"
  license "GPL-3.0-or-later"
  version "4.0.2"
  depends_on "fontconfig"

  on_macos do
    on_arm do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.2/utuimp_darwin_arm64.tar.gz"
      sha256 "2e169750cdfabf6ab615c21065e0b58d1fc5603c139803384f88e9f86baab0f9"
    end
    on_intel do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.2/utuimp_darwin_amd64.tar.gz"
      sha256 "656e1f95061be2a3465481e48492042c9ec9a9e8f3acf3a1f97a126ec974431c"
    end
  end

  on_linux do
    depends_on "gstreamer"
    depends_on arch: :x86_64
    url "https://github.com/tphx37/utuimp/releases/download/v4.0.2/utuimp_linux_amd64.tar.gz"
    sha256 "2c00f01a42b1f38cd2cb43508c78a0458325b6e84f260e859d8b64ebfd1b51cc"
  end

  def install
    bin.install "utuimp"
    prefix.install "NOTICE"
  end

  def caveats
    "For YouTube Music and SoundCloud: brew install yt-dlp ffmpeg\nFor Spotify Premium: brew install librespot"
  end
end
