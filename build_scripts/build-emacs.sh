#!/bin/bash

[ -z "${EMACS_SOURCE_PATH}" ] && echo Error. Set EMACS_SOURCE_PATH. && exit 1

[ -z "${EMACS_PREFIX}" ] && EMACS_PREFIX=/usr

${EMACS_SOURCE_PATH}/configure\
	--prefix=${EMACS_PREFIX}\
	--without-all\
	--with-x\
	--with-x-toolkit=gtk3\
	--with-xml2\
	--with-json\
	--with-cairo\
	--with-harfbuzz\
	--with-toolkit-scroll-bars\
	--with-xdbe\
	--with-gpm\
	--with-dbus\
	--with-gnutls\
	--with-zlib\
	--with-modules\
	--with-threads\
	--with-file-notification=inotify\
	--with-libgmp

