#!/bin/sh
# Build a signed, static pacman repository suitable for GitHub Pages.
# Usage: UTUIMP_SIGNING_KEY=<fingerprint> sh scripts/build-pacman-repo.sh <site-dir> <package>...
set -eu
[ "$#" -ge 2 ] || { echo "usage: UTUIMP_SIGNING_KEY=<fingerprint> $0 <site-dir> <package>..." >&2; exit 1; }
: "${UTUIMP_SIGNING_KEY:?set UTUIMP_SIGNING_KEY to your GPG signing key fingerprint}"
for command in repo-add gpg bsdtar; do
    command -v "$command" >/dev/null || { echo "$command is required" >&2; exit 1; }
done
site=$1
shift
mkdir -p "$site/x86_64"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM
for database in utuimp.db.tar.gz utuimp.files.tar.gz; do
    if [ -f "$site/x86_64/$database" ]; then
        cp "$site/x86_64/$database" "$work/$database"
    fi
done
for package do
    arch=$(bsdtar -xOf "$package" .PKGINFO | sed -n 's/^arch = //p')
    [ "$arch" = x86_64 ] || { echo "expected x86_64 package: $package" >&2; exit 1; }
    name=$(basename "$package")
    cp "$package" "$work/$name"
    gpg --batch --yes --local-user "$UTUIMP_SIGNING_KEY" --detach-sign "$work/$name"
    (cd "$work" && repo-add --sign --key "$UTUIMP_SIGNING_KEY" utuimp.db.tar.gz "$name")
    cp "$work/$name" "$work/$name.sig" "$site/x86_64/"
done
# Serve ordinary files: Pages does not need to resolve repo-add's symlinks.
for file in utuimp.db.tar.gz utuimp.db.tar.gz.sig utuimp.files.tar.gz utuimp.files.tar.gz.sig; do
    cp "$work/$file" "$site/x86_64/$file"
done
cp "$work/utuimp.db.tar.gz" "$site/x86_64/utuimp.db"
cp "$work/utuimp.db.tar.gz.sig" "$site/x86_64/utuimp.db.sig"
cp "$work/utuimp.files.tar.gz" "$site/x86_64/utuimp.files"
cp "$work/utuimp.files.tar.gz.sig" "$site/x86_64/utuimp.files.sig"
gpg --armor --export "$UTUIMP_SIGNING_KEY" > "$site/utuimp-repo.asc"
touch "$site/.nojekyll"
echo "Repository ready at $site; publish it with GitHub Pages."
