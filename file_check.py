filename = "dummy_file.txt"

with open(filename, 'r') as f:
	count = 0
	for row in f:
		count += 1
	print(count)
