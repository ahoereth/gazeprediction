SRC=$(wildcard **/*.md)
PHONYS=$(SRC:.md=)

all: $(PHONYS)

$(PHONYS):
	pandoc $@.md -o $@.pdf
