#! python3

# DATA ANALYSIS

import numpy as np
import datetime
import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pyplot_themes as themes
import pandas as pd
pd.set_option('mode.chained_assignment', None)


# ANALYSIS AND STATISTICS

def round_to(weight, precision = 0.1):
	# Round number to closest 0.1 kg
	remainder = weight % precision
	if remainder < (precision / 2):
		return (weight - remainder)
	else:
		return (weight + (precision - remainder))


def infer_missing_data(df_infer):
	last_i = len(df_infer.weight)
	for i, w in enumerate(df_infer.weight):
		if pd.isna(w):
			w_1 = df_infer.weight[i - 1]
			j = i + 1

			# Number of missing weight in a row
			w_miss = 1

			while j < last_i and pd.isna(df_infer.weight[j]):
				j += 1
				w_miss += 1

			# If last value is NaN infer last valid weight
			if j == last_i:
				w_2 = w_1
			else:
				w_2 = df_infer.weight[j]

			# Daily difference between consecutive days
			diff_daily = (w_2 - w_1) / (w_miss + 1)

			# Replace inferred values
			for i_miss in range(i, j):
				value_miss = w_1 + (diff_daily * (i_miss - i + 1))
				value_rounded = round_to(value_miss, 0.1)
				df_infer.weight.iloc[i_miss] = value_rounded
	return df_infer


def moving_average(df_ma, window_width = 4):
	# Calculate moving average
	cumsum_vec = np.cumsum(np.insert(list(df_ma.weight), 0, 0))
	ma_vec = (cumsum_vec[window_width:] - cumsum_vec[:-window_width]) / window_width

	df_ma = df_ma[(window_width - 1):]
	df_ma.weight = ma_vec
	return df_ma


def calculate_stats(df_infer):
	last_weight = list(df_infer.weight)[-1]
	'''
	# Past weights relative to today (not used)
	weight_1m = list(df_infer.weight)[-31]
	weight_2m = list(df_infer.weight)[-61]
	weight_6m = list(df_infer.weight)[-181]
	weight_1y = list(df_infer.weight)[-366]
	'''
	# Max, min, median last 30 days
	df_30gg = df_infer[-30:].copy()
	max_30gg = df_30gg[df_30gg.weight == df_30gg.weight.max()]
	min_30gg = df_30gg[df_30gg.weight == df_30gg.weight.min()]
	median_30gg = df_30gg.weight.median()


	# DataFrame moving average last 30 days
	df_ma = df_infer.copy()
	df_ma = moving_average(df_ma)
	ma_30gg = df_ma[-30:].copy()
	
	return last_weight, df_30gg, max_30gg, min_30gg, median_30gg, ma_30gg


def save_stats(last_weight, DATE_TODAY, max_30gg, min_30gg, median_30gg):
	report_statistics = {
		'last_weight': last_weight,
		'date': DATE_TODAY,
		'max': float(max_30gg.weight[:]),
		'min': float(min_30gg.weight[:]),
		'median': median_30gg}

	with open('report_statistics.pickle', 'wb') as f:
		pickle.dump(report_statistics, f, protocol=pickle.HIGHEST_PROTOCOL)
	print('Statistics saved in "report_statistics.pickle".')


def plot_sparkline(df_infer):
	plt.figure(1)
	fig1, ax1 = plt.subplots(1,1,figsize=(12.8, 2.3))  # figsize=(12.8, 2.3)
	plt.plot(df_infer.date[:], df_infer.weight[:], color='k')
	plt.plot(df_infer.date.iloc[-1], df_infer.weight.iloc[-1],
		'x', color='r') # marker='o'

	# remove all the axes
	for k,v in ax1.spines.items():
		v.set_visible(False)
	ax1.set_xticks([])
	ax1.set_yticks([])

	plt.margins(0.0)
	fig1.tight_layout()

	# Save chart
	fig1.savefig('charts/sparkline.png', dpi=100, pad_inches=0.0)
	print('Plot "sparkline.png" saved.')
	return


def plot_30days(df_30gg, ma_30gg, min_30gg, max_30gg):
	days = mdates.DayLocator()
	mondays = mdates.WeekdayLocator(byweekday=0)
	days_fmt = mdates.DateFormatter('%d-%m')

	plt.figure(2)
	fig2, ax2 = plt.subplots(1,1,figsize=(6.7, 3.5))  # figsize=(11.5, 6)  7.7, 4

	ax2.xaxis.set_major_locator(mondays)
	ax2.xaxis.set_major_formatter(days_fmt)
	ax2.xaxis.set_minor_locator(days)

	# Hide top and right side of the frame
	ax2.spines['right'].set_visible(False)
	ax2.spines['top'].set_visible(False)

	plt.grid(b=True, which='major', color='#D3D3D3', linestyle='--')  # #666666
	plt.minorticks_off()

	ax2.plot('date', 'weight', data=df_30gg, color='black', linewidth=2.0)
	ax2.plot('date', 'weight', data=ma_30gg, color='white', linewidth=5.0, linestyle='--')
	ax2.plot('date', 'weight', data=ma_30gg, color='red',   linewidth=2.0, linestyle='--')
	plt.ylim(float(min_30gg.weight[:]) - 0.5, float(max_30gg.weight[:]) + 0.5)

	ax2.format_xdata = mdates.DateFormatter('%d/%m/%Y')

	# Add max and min labels
	xytext_value = (0,6)
	for df_label in [max_30gg, min_30gg]:
		plt.annotate(
			str(df_label.weight.iloc[0]),
			(df_label.date.iloc[0], df_label.weight.iloc[0]),
			textcoords="offset points", # how to position the text
			xytext=xytext_value, # distance from text to points (x,y)
			ha='center'
			)
		plt.plot(
			df_label.date.iloc[0], df_label.weight.iloc[0],
			'x', color='red', # marker='o'
			)
		xytext_value = (0,-16)

	plt.margins(0.0)
	fig2.tight_layout()

	# Save chart
	fig2.savefig('charts/chart_30days.png', dpi=100, pad_inches=0.0)
	print('Plot "chart_30days.png" saved.')
	return


def plot_weekdays(df_infer):
	df_90gg = df_infer[-90:].copy()
	df_90gg['weekday'] = df_90gg.date.dt.weekday
	mean_90gg = round(df_90gg.weight.mean(), 2)
	week_df = round(df_90gg.groupby(df_90gg.date.dt.weekday).mean(), 2)
	week_df['weight'] = week_df['weight'] - mean_90gg
	week_df['weekday'] = range(7)

	plt.figure(3)
	fig3, ax3 = plt.subplots(1,1,figsize=(6.7, 3.5))  # figsize=(11.5, 6)

	plt.hlines(mean_90gg, xmin = -0.75, xmax= 6.75,
		linestyles='dashed', linewidths=0.5,
		colors='black')
	plt.plot(df_90gg.weekday[:], df_90gg.weight[:], 'x', 
		alpha=0.8, color='black')
	plt.bar(week_df.weekday[:], week_df.weight[:], 
		color='red', bottom=mean_90gg, alpha=1.0)

	# Hide top and right side of the frame
	ax3.spines['right'].set_visible(False)
	ax3.spines['top'].set_visible(False)

	plt.grid(b=True, axis='y', which='major', color='#D3D3D3', linestyle='--')
	plt.minorticks_off()

	plt.xticks(week_df.weekday[:], 
		['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
		'Friday', 'Saturday', 'Sunday'],
		rotation=15) # rotation=35

	plt.margins(0.0)
	fig3.tight_layout()

	# Save plot
	fig3.savefig('charts/chart_weekdays.png', dpi=100, pad_inches=0.0)
	print('Plot "chart_weekdays.png" saved.')
	return


def save_plots(df_infer, df_30gg, ma_30gg, min_30gg, max_30gg):
	# Sparkline
	plot_sparkline(df_infer)

	# Plot 30 days
	plot_30days(df_30gg, ma_30gg, min_30gg, max_30gg)

	# Chart by weekday for last 90 days
	plot_weekdays(df_infer)


def main():
	DATE_TODAY = datetime.date.today().strftime('%d/%m/%Y')
	DATE_CODE = datetime.date.today().strftime('%Y%m%d')
	CSV_NAME = f'weight_data_{DATE_CODE}.csv'

	df = pd.read_csv(f'data/{CSV_NAME}', decimal=',')
	df.date = pd.to_datetime(df.date, format='%d/%m/%Y')

	# DataFrame with inferred data
	df_infer = df.copy()
	df_infer = infer_missing_data(df_infer)

	# Calculate statistics
	last_weight, df_30gg, max_30gg, min_30gg, median_30gg, ma_30gg = calculate_stats(df_infer)

	# Save statistics in pickle file
	save_stats(last_weight, DATE_TODAY, max_30gg, min_30gg, median_30gg)

	# Create and save charts
	save_plots(df_infer, df_30gg, ma_30gg, min_30gg, max_30gg)


if __name__ == '__main__':
	main()