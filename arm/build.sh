TARGET=arm-none-eabi-
AS=${TARGET}as
GCC=${TARGET}gcc
LINK=${TARGET}ld
OBC=${TARGET}objcopy

THUMB=""
AS_FLAGS="-mcpu=cortex-a7 -march=armv7-a ${THUMB} -EL"
LINK_FLAGS="-T link.ld"
OBC_FLAGS="-S -O binary -R .ARM.attributes"

${AS} ${AS_FLAGS} start.s -o start.o
${LINK} ${LINK_FLAGS} start.o -o main.elf
${OBC} ${OBC_FLAGS} main.elf main.bin
