import glob
from setuptools import archive_util
import gzip
import glob
import os

for fn in glob.glob('*.gz'):
	inF = gzip.open(fn, 'rb')
 	outFilename = 'un'+fn[0:-3]
	outF = open(outFilename, 'wb')
	outF.write( inF.read() )
	inF.close()
	outF.close()