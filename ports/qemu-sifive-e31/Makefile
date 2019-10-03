#
# Copyright © 2019 Keith Packard <keithp@keithp.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#

SNEK_ROOT = ../..

SNEK_FE310 = $(SNEK_ROOT)/chips/fe310

PROGNAME=snek-e31
PRODUCT_NAME=snek-e31

include $(SNEK_FE310)/snek-fe310.defs

SNEK_EXTRA_SRC = \

SNEK_LOCAL_SRC = \
	inline.c \
	fixed-clock.c \
	riscv_plic0.c \
	riscv_clint0.c \
	riscv_cpu.c \
	sifive_fe310-g000_prci.c \
	sifive_fe310-g000_hfrosc.c \
	sifive_fe310-g000_hfxosc.c \
	sifive_fe310-g000_lfrosc.c \
	sifive_fe310-g000_pll.c \
	sifive_uart0.c \
	sifive_spi0.c \
	sifive_gpio-leds.c \
	sifive_wdog0.c \
	sifive_rtc0.c \
	sifive_gpio0.c \
	sifive_local-external-interrupts0.c \
	$(SNEK_FE310_SRC)

SNEK_LOCAL_INC = \
	$(SNEK_FE310_INC)

SNEK_LOCAL_BUILTINS = \
	$(SNEK_FE310_BUILTINS) \
	snek-e31.builtin

include $(SNEK_ROOT)/snek-install.defs

SRC=$(SNEK_SRC)
OBJ=$(patsubst %.S,%.o,$(patsubst %.c,%.o,$(SRC)))

all: $(PROG) $(BIN)

$(PROG): Makefile $(OBJ)
	$(call quiet,CC) $(LDFLAGS) -Te31.ld -Wl,-M=$(MAP) -o $@ $(OBJ) $(LIBS)

$(OBJ): $(SNEK_INC)

distclean:	clean

clean::
	rm -f *.o $(PROGNAME)*.elf $(PROGNAME)*.bin $(PROGNAME)*.map ao-product.h
	rm -f snek-board-install

snek-board-install: snek-board-install.in
	$(SNEK_SED) $^ > $@
	chmod +x $@

echo:
	echo PROG is $(PROG)

install: $(PROG)
	install -d $(DESTDIR)$(SHAREDIR)
	install -m 0644 $(PROG) $(DESTDIR)$(SHAREDIR)

uninstall:
