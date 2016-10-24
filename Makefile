SRC=$(wildcard **/*.md)
DST=$(SRC:.md=.pdf)

all: $(DST)

$(DST):
	 pandoc $(@:.pdf=.md) -o $@
