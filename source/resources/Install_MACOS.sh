#!/bin/bash
echo "Initializing"
pkgPath="$HOME/Library/Application Support/espanso/match/packages/good-morning/"
echo ..

# Remove any existing copies of package:
echo "Removing any existing package data"
if [ -e "$pkgPath" ]; then rm -r "$pkgPath"; fi

# Create package directory:
echo "Creating package directory"
mkdir -p "$pkgPath/resources"

# Copy files to package directory:
echo "Installing package"
cp "../good-morning.yml" "$pkgPath"
cp -a "../resources/" "$pkgPath/resources/"

echo "Cleaning up"

# Overwrite Windows yml file with MacOS yml file:
mv "$pkgPath"/resources/good-morning.yml_MACOS "$pkgPath"/good-morning.yml

# Remove any files related to windows:
rm "$pkgPath"/resources/*_WINDOWS*

# Remove install files from package directory:
rm "$pkgPath"/resources/Install_*

echo "Finished"

