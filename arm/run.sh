#!/bin/bash

# 		-drive file=boot.img,format=raw \
qemu-system-arm -machine virt \
	        -cpu cortex-a8 \
		-m size=1024 \
		-kernel boot.img \
		-s -S \
		-display none \
		-chardev tty,id=serialdev,path=/dev/tty11 \
		-serial stdio \
		-monitor chardev:serialdev
		
