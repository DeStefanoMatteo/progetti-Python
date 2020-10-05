#! python3
# BENCH PRESS ONE REP MAX

'''
Formula
https://www.unm.edu/~rrobergs/478RMStrengthPrediction.pdf

Bryzcki
1RM = weight / (1.0278 - (0.0278 * reps))
weight = 1RM * (1.0278 - (0.0278 * reps))

O'Connor
1RM = (0.025 * (weight * reps)) + weight

Formula
%1RM = 55.51 * e^(-0.0723 * reps) + 48.47
reps = (log(((1RM - 48.47) / 55.51)))/-0.0723
'''

from math import exp
import os

def check_float(number):
	try:
		number = float(number)
		return True
	except ValueError:
		return False

def round_to(weight, precision = 0.25):
	# Round number to closest 0.25 kg
	remainder = weight % precision
	if remainder < (precision / 2):
		return (weight - remainder)
	else:
		return (weight + (precision - remainder))


def rm_bryzcki(weight, reps):
	# Estimate 1RM using Bryzcki formula
	return weight / (1.0278 - (0.0278 * reps))

def rm_oconnor(weight, reps):
	# Estimate 1RM using O'Connor formula
	return (0.025 * (weight * reps)) + weight

def rm_mean(weight, reps):
	# Estimate 1RM as the mean between Bryzcki and O'Connor results
	return round((rm_bryzcki(weight, reps) + rm_oconnor(weight, reps)) / 2, 2)

def rm_table(rm):
	rep_range = range(2, 21)
	rm_range = {}

	for rep in rep_range:
		# calcolo percentuale del RM per rep
		perc_rm = (55.51 * exp(-0.0723 * rep) + 48.47) / 100
		rm_rep = rm * perc_rm

		rm_range[rep] = round(rm_rep, 2)
	return rm_range



# Input
os.system('cls')
print('\nCalculate Your Bench Press One Rep Max (1RM)')
print('Enter weight and reps of your maxed set.\n')

weight = input('Weight (kg): ')

# Format check
while check_float(weight) == False:
	print('Enter a number.')
	weight = input('Weight (kg): ')
weight = float(weight)

reps = input('Reps:        ')

# Format check
while reps.isdigit() == False:
	print('Enter a integer.')
	reps = input('Reps:        ')
reps = float(reps)

# Estimate 1RM
rm_mean = rm_mean(weight, reps)

# Print 1RM
print('\n\n################')
print(f'\n 1RM: {round_to(rm_mean):.2f} kg\n')
print('################\n')

# Calculate table of RM
rm_range = rm_table(rm_mean)

# Print table
print('Reps   Weight (kg)')
print(f'{1:>3}: {round_to(rm_mean):>8.2f}')
for el in rm_range:
	print(f'{el:>3}: {round_to(rm_range[el]):>8.2f}')

# Keep window open
input()
