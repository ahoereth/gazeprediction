report:
	pandoc \
		-f markdown+multiline_tables \
		-o report_zivkovi2006_seasquirt.pdf \
		--bibliography=report.bib \
		report.md

slides:
	echo "No slides yet."

zip: report slides
	zip -r Task3_seasquirt.zip \
		report_zivkovi2006_seasquirt.pdf

