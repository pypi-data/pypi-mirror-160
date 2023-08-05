SCL=$(wildcard *.scl)
PDF=$(SCL:.scl=.pdf)

main: $(PDF)

.ONESHELL:
%.tex: %.scl
	export PYTHONPATH="$${PYTHONPATH}:$$(cd ../.. && pwd)"
	python3 -m scal $< > $@

%.pdf: %.tex
	spix $<
