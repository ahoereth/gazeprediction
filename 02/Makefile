results:
	python gabor_saliency.py 640x480/test0.jpg
	python gabor_saliency.py 384x384/test1.jpg
	python gabor_saliency.py 384x384/test2.jpg
	python gabor_saliency.py 500x357/voc2012_000122.jpg
	python gabor_saliency.py 500x357/voc2012_000138.jpg
report: results
	pandoc -f markdown+tex_math_dollars -o report_task2_seasquirt.pdf --bibliography=report.bib report.md
zip: report
	zip -r Task2_seasquirt.zip slides_task2_seasquirt.ipynb report_task2_seasquirt.pdf task2.ipynb gabor_saliency.py
