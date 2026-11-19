class Utuimp < Formula
  desc "Universal terminal user interface media player"
  homepage "https://github.com/tphx37/utuimp"
  license "GPL-3.0-or-later"
  version "4.0.3"
  depends_on "fontconfig"

  on_macos do
    on_arm do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.3/utuimp_darwin_arm64.tar.gz"
      sha256 "fbadd0a1793068be115f180e5d4c9eb3d0f8caf947445f9a27d40ae6d22d745b"
    end
    on_intel do
      url "https://github.com/tphx37/utuimp/releases/download/v4.0.3/utuimp_darwin_amd64.tar.gz"
      sha256 "a23ec0c46a8e72b58bf9542f60d165a252657cff82e6767a98f14010930bb344"
    end
  end

  on_linux do
    depends_on "gstreamer"
    depends_on arch: :x86_64
    url "https://github.com/tphx37/utuimp/releases/download/v4.0.3/utuimp_linux_amd64.tar.gz"
    sha256 "baaa88cee46206cd9af19461d6b6c7adb3d8f009ac9d78ee6cddcb9c26674cdd"
  end

  def install
    bin.install "utuimp"
    prefix.install "NOTICE"
  end

  def caveats
    "For YouTube Music and SoundCloud: brew install yt-dlp ffmpeg\nFor Spotify Premium: brew install librespot"
  end
end
