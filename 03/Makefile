all: report slides zip

report:
	pandoc \
		-f markdown+multiline_tables \
		-o report_zivkovic2006_seasquirt.pdf \
		--bibliography=report.bib \
		report.md

slides:
	pandoc \
		-t beamer \
		-f markdown+multiline_tables \
		-o slides_zivkovic2006_seasquirt.pdf \
		--bibliography=report.bib \
		--slide-level=2 \
		--listings \
		slides.md

zip: report slides
	zip -r Task3_seasquirt.zip \
		ComparisonBackgroundSubtraction.ipynb \
		report_zivkovic2006_seasquirt.pdf
