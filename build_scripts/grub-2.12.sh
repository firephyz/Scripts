#!/bin/bash

. build

<EOS
#  --build=BUILD     configure for building on BUILD [guessed]
  --host=x86_64-pc-linux-gnu
  --target=x86_64-pc-linux-gnu

# Optional Features:
#   --disable-option-checking  ignore unrecognized --enable/--with options
#   --disable-FEATURE       do not include FEATURE (same as --enable-FEATURE=no)
#   --enable-FEATURE[=ARG]  include FEATURE [ARG=yes]
#   --enable-dependency-tracking
#                           do not reject slow dependency extractors
#   --disable-dependency-tracking
#                           speeds up one-time build
#   --enable-silent-rules   less verbose build output (undo: "make V=1")
#   --disable-silent-rules  verbose build output (undo: "make V=0")
#   --disable-largefile     omit support for large files
#   --disable-year2038      omit support for timestamps past the year 2038
  # --disable-threads
  #                         specify multithreading API
  --disable-threads
  # --disable-nls           do not use Native Language Support
  # --disable-rpath         do not hardcode runtime library paths
  # --enable-cross-guesses={conservative|risky}
  #                         specify policy for cross-compilation guesses
  --disable-efiemu
  --enable-stack-protector
  # --enable-mm-debug       include memory manager debugging
  # --enable-cache-stats    enable disk cache statistics collection
  # --enable-boot-time      enable boot time statistics collection
  # --enable-grub-emu-sdl2  build and install the `grub-emu' debugging utility
  #                         with SDL2 support (default=guessed)
  # --enable-grub-emu-sdl   build and install the `grub-emu' debugging utility
  #                         with SDL support (default=guessed)
  # --enable-grub-emu-pci   build and install the `grub-emu' debugging utility
  #                         with PCI support (potentially dangerous)
  #                         (default=no)
  --enable-grub-mkfont
  --disable-grub-themes
  --enable-grub-mount
  --enable-device-mapper
  # --enable-liblzma        enable liblzma integration (default=guessed)
  # --enable-libzfs         enable libzfs integration (default=guessed)
  --disable-werror

# Optional Packages:
#   --with-PACKAGE[=ARG]    use PACKAGE [ARG=yes]
#   --without-PACKAGE       do not use PACKAGE (same as --with-PACKAGE=no)
  --with-platform=efi
  # --with-bootdir=DIR      set the name of /boot directory [[guessed]]
  # --with-grubdir=DIR      set the name of grub directory [[guessed]]
  # --with-gnu-ld           assume the C compiler uses GNU ld [default=no]
  # --with-libiconv-prefix[=DIR]  search for libiconv in DIR/include and DIR/lib
  # --without-libiconv-prefix     don't search for libiconv in includedir and libdir
  # --with-libintl-prefix[=DIR]  search for libintl in DIR/include and DIR/lib
  # --without-libintl-prefix     don't search for libintl in includedir and libdir
  # --without-included-regex
  #                         don't compile regex; this is the default on systems
  #                         with recent-enough versions of the GNU C Library
  #                         (use with caution on other systems).
  # --with-dejavufont=FILE  set the DejeVu source [[guessed]]
  # --with-unifont=FILE     set the unifont source [[guessed]]
