#Sample_data
# Script for generating smaller samples of the data
import os
import numpy as np
import random


target_dir = '../Toy Data/'

print('Deleting Target Files')
file_names = os.listdir(target_dir)
for file in file_names:
	os.remove(target_dir + file)


print('Done')
print('')

number_of_files = 10
number_of_lines = 1000

print('Starting Process')
print('Number of Files: ' + str(number_of_files))
print('Number of Lines per File: ' + str(number_of_lines))


file_names = os.listdir()
file_names.remove('sample_data.py')
np.random.shuffle(file_names)

def get_rand_name():
	return(file_names[np.random.randint(len(file_names))])

print('')
for i in np.arange(number_of_files):
	print('Started File: ' + str(i+1))

	file = open(target_dir + 'sample_' + str(i+1) + '.csv', 'w')

	# Writes Header
	temp_file = open(get_rand_name(),'r')
	file.write(temp_file.readline() + '\n')
	temp_file.close()
	if(np.random.rand() < 0.5):
		file.write('\n')

	

	lines_out = 0
	while(lines_out < number_of_lines):
		batch = np.random.randint(number_of_lines - lines_out + 10)
		temp_name = get_rand_name()
		with open(temp_name,'r') as temp_file:

			lines = temp_file.readlines()
			for k in np.arange(batch):
				file.write(random.choice(lines))

			lines_out = lines_out + batch

	file.write('\n')
	file.close()
	print('Finished')
	print('')

print('')



	
 


