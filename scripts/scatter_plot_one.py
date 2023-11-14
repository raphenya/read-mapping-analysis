"""
 Copyright (c) 2019-2023 Amogelang R. Raphenya

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def main(args):
	# Load the dataset
	df = pd.read_csv(args.input_file, sep="\t")
	# filters
	#df = df[df['Completely Mapped Reads'] >= int(args.reads_count)]
	df = df[df['Average Percent Coverage'] >= float(args.coverage)]
	#df = df[df['Average MAPQ (Completely Mapped Reads)'] >= float(args.mapq)]

	# splot by specific amr gene family
	if args.plot == "specific_amr_gene_family":
		df = df[df['AMR Gene Family'].str.contains(args.one_family)]
		svm2 = sns.relplot(
			x="Completely Mapped Reads", 
			y="Average Percent Coverage", 
			hue="AMR Gene Family",
			size="Average MAPQ (Completely Mapped Reads)",
			sizes=(40, 400), 
			alpha=.5, 
			palette="muted", 
			height=6, 
			data=df,
		)

	if args.plot == "amr_gene_family":
		svm2 = sns.relplot(
			x="Completely Mapped Reads", 
			y="Average MAPQ (Completely Mapped Reads)", 
			hue="AMR Gene Family",
			size="Average Percent Coverage",
			sizes=(40, 400), 
			alpha=.5, 
			palette="muted", 
			height=6, 
			data=df,
		)

	if args.plot == "aro_term":
		# OXA-1 , AAC(6')-Ib-cr, NDM-1, QnrB1, catI, CTX-M-15
		# filtered = df[df['AMR Gene Family'].str.contains("CTX-M")]

		svm2 = sns.relplot(
			x="Completely Mapped Reads", 
			y="Average MAPQ (Completely Mapped Reads)", 
			hue="ARO Term",
			size="Average Percent Coverage",
			sizes=(40, 400), 
			alpha=.5, 
			palette="muted", 
			height=6, 
			data=df,
		)

	# add cut off lines
	#plt.axvline(x=int(args.reads_count), ymin=0, ymax=1, color="red")
	#plt.axhline(y=float(args.mapq), xmin=0, xmax=1, color="blue")

	# save plot to image file
	plt.savefig(args.output_file+'.png', dpi=400)

def create_parser():
	parser = argparse.ArgumentParser(prog="scatter_plot", description="scatter plot")
	parser.add_argument('-i', '--input_file', required=False, help='tab input file')
	parser.add_argument('-o', '--output_file', required=False, help='png output file')
	parser.add_argument('-n', '--reads_count', required=False, default=20, help="filter by reads count")
	parser.add_argument('-c', '--coverage', required=False, default=90, help="filter by coverage")
	parser.add_argument('-q', '--mapq', required=False, default=0, help="filter by mapq")
	parser.add_argument('--one_family', required=False, default="", help="filter by one amr gene family e.g 'NDM beta-lactamase'")
	parser.add_argument('-p','--plot', dest="plot", default="aro_term",
	                	choices=['aro_term', 'amr_gene_family', 'specific_amr_gene_family'],
	                	help = "specify a category (default = aro_term)")
	return parser

def run():
	parser = create_parser()
	args = parser.parse_args()
	main(args)

if __name__ == "__main__":
	run()
