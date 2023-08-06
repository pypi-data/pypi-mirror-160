# 2022.7.27
import json, traceback,sys, time,  fileinput #https://docs.python.org/3/library/fileinput.html

def walk(infile): 
	''' gzjc.json340.gz '''
	#for line in fileinput.hook_compressed(infile,fileinput.hook_compressed): 
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		print (line) 

def tojson(infile, outfile=None):
	''' gzjc.snt => gzjc.json340'''
	import spacy 
	nlp =spacy.load('en_core_web_sm')
	if outfile is None: outfile = infile.split('.')[0] + ".json340"
	with open(outfile, 'w') as fw: 
		for line in fileinput.input(infile):
			doc = nlp(line.strip().split('\t')[-1].strip()) 
			res = doc.to_json() 
			fw.write( json.dumps(res) + "\n")
	print ("finished:", infile ) 

if __name__	== '__main__':
	import fire 
	fire.Fire()
