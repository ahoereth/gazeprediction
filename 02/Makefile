report:
	pandoc -f markdown+tex_math_dollars -o report_task2_seasquirt.pdf --bibliography=report.bib report.md
slides:
	cp slides.ipynb slides_task2_seasquirt.ipynb
zip: report slides
	zip -r Task2_seasquirt.zip slides_task2_seasquirt.ipynb report_task2_seasquirt.pdf task2.ipynb gabor_saliency.py
