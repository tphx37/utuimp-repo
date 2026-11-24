class Utuimp < Formula
  desc "Universal terminal user interface media player"
  homepage "https://github.com/tphx37/utuimp"
  license "GPL-3.0-or-later"
  version "4.0.4"
  depends_on "fontconfig"

  on_macos do
    on_arm do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.4/utuimp_darwin_arm64.tar.gz"
      sha256 "f92c07d254aba4612bd34975241163229052ca9fd4299925ec8973850d89bbd2"
    end
    on_intel do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.4/utuimp_darwin_amd64.tar.gz"
      sha256 "da566fa4335e0bd7be9652edae1ab456e1b7004c2c4dfa31aa0b4f5c7d6ff444"
    end
  end

  on_linux do
    depends_on "gstreamer"
    depends_on arch: :x86_64
    url "https://github.com/tphx37/utuimp/releases/download/v4.0.4/utuimp_linux_amd64.tar.gz"
    sha256 "3993fd89efc22d3e3007144013ecef9bed9d70750b9487367952004ea470f6d7"
  end

  def install
    bin.install "utuimp"
    prefix.install "NOTICE"
  end

  def caveats
    "For YouTube Music and SoundCloud: brew install yt-dlp ffmpeg\nFor Spotify Premium: brew install librespot"
  end
end
