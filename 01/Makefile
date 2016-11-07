all: zip
report:
	pandoc -f markdown+tex_math_dollars -o report_achanta2009_seasquirt.pdf --bibliography=report.bib report.md
slides:
	pdflatex slides.tex
	bibtex slides
	pdflatex slides.tex
	pdflatex slides.tex
	mv slides.pdf slides_achanta2009_seasquirt.pdf
zip: report slides
	zip -r achanta2009_seasquirt.zip slides_achanta2009_seasquirt.pdf report_achanta2009_seasquirt.pdf images

