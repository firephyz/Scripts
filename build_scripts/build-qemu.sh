if [[ -z ${QEMU_SRC_PATH} ]]; then
    echo Set QEMU_SRC_PATH
    exit 1
else
    QEMU_SRC_PATH=$(readlink -f ${QEMU_SRC_PATH})
fi

#test -z ${QEMU_BUILD_PATH} && QEMU_BUILD_PATH=$(readlink -f $(pwd)/qemu-build)
test -z ${QEMU_BUILD_PATH} && QEMU_BUILD_PATH=$(readlink -f ~/builds/qemu)

mkdir -p $QEMU_BUILD_PATH
cd $QEMU_BUILD_PATH

# USER_TARGET_LIST=,aarch64-linux-user,arm-linux-user,riscv32-linux-user,riscv64-linux-user
USER_TARGET_LIST=

${QEMU_SRC_PATH}/configure \
		--prefix=/home/kyle/programs/root \
		--target-list=aarch64-softmmu,arm-softmmu,riscv32-softmmu,riscv64-softmmu${USER_TARGET_LIST} \
		--audio-drv-list= \
		--disable-strip \
		--enable-trace-backends=simple \
		--enable-tcg-interpreter \
		--enable-system \
		--disable-user \
		--disable-linux-user \
		--disable-bsd-user \
		--disable-docs \
		--disable-guest-agent \
		--disable-guest-agent-msi \
		--disable-pie \
		--disable-modules \
		--disable-debug-tcg \
		--enable-debug-info \
		--disable-sparse \
		--disable-gnutls \
		--disable-nettle \
		--disable-gcrypt \
		--disable-auth-pam \
		--disable-sdl \
		--disable-sdl-image \
		--disable-gtk \
		--disable-vte \
		--enable-curses \
		--enable-iconv \
		--disable-vnc \
		--disable-vnc-sasl \
		--disable-vnc-jpeg \
		--disable-vnc-png \
		--disable-cocoa \
		--disable-virtfs \
		--disable-mpath \
		--disable-xen \
		--disable-xen-pci-passthrough \
		--disable-brlapi \
		--disable-curl \
		--disable-membarrier \
		--enable-fdt \
		--enable-kvm \
		--disable-hax \
		--disable-hvf \
		--disable-whpx \
		--disable-rdma \
		--disable-pvrdma \
		--disable-vde \
		--disable-netmap \
		--disable-linux-aio \
		--disable-cap-ng \
		--disable-attr \
		--disable-vhost-net \
		--disable-vhost-vsock \
		--disable-vhost-scsi \
		--disable-vhost-crypto \
		--disable-vhost-kernel \
		--disable-vhost-user \
		--disable-spice \
		--disable-rbd \
		--disable-libiscsi \
		--disable-libnfs \
		--disable-smartcard \
		--disable-libusb \
		--disable-live-block-migration \
		--disable-usb-redir \
		--disable-lzo \
		--disable-snappy \
		--disable-bzip2 \
		--disable-lzfse \
		--disable-seccomp \
		--disable-coroutine-pool \
		--disable-glusterfs \
		--disable-tpm \
		--disable-libssh \
		--disable-numa \
		--disable-libxml2 \
		--disable-tcmalloc \
		--disable-jemalloc \
		--disable-avx2 \
		--disable-replication \
		--disable-opengl \
		--disable-virglrenderer \
		--disable-xfsctl \
		--disable-qom-cast-debug \
		--enable-tools \
		--enable-bochs \
		--disable-cloop \
		--disable-dmg \
		--disable-qcow1 \
		--disable-vdi \
		--disable-vvfat \
		--disable-qed \
		--disable-parallels \
		--disable-crypto-afalg \
		--disable-capstone \
		--disable-debug-mutex \
		--disable-libpmem \
		--disable-xkbcommon
