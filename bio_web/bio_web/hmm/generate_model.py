import hmmlib

f = open("lncRNA_Seed.txt")

seqs = []
family_name = ""
for line in f:
	if line[0:2] == "RF" :
		if len(seqs) == 0:
			family_name = line.strip()
			continue
		hmmlib.makeModel(seqs, family_name)
		family_name = line.strip()
		seqs = []
	else:
		seqs.append(line.strip())
hmmlib.makeModel(seqs, family_name)