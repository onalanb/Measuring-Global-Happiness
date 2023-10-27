import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the list of CSV files for different years
file_paths = []
cwd = os.getcwd()
for year in range(2015, 2023):
    path = os.path.join(cwd, 'Data')
    path = os.path.join(path, str(year) + '.csv')
    file_paths.append(path)

# Read the first CSV and drop everything except for countries and regions, everything will join to this data frame.
all_years = pd.read_csv(file_paths[0])
columns_to_drop = [col for col in all_years.columns if col in all_years.columns and not (col in ['Country', 'Region'])]
all_years.drop(columns_to_drop, axis=1, errors='ignore', inplace=True)

# Loop through the list of file paths and process the data for each year.
for file_path in file_paths:
    year = file_path.split(os.path.sep)[-1].split('.csv')[0]
    data = pd.read_csv(file_path)
    # Copying 'Happiness Score' column into a new column with column name as year.
    data[year] = data['Happiness Score']
    # Drop all columns except for country and year.
    columns_to_drop = [col for col in data.columns if col in data.columns and not (col in ['Country', year])]
    data.drop(columns_to_drop, axis=1, errors='ignore', inplace=True)
    # Merge this years data to all year data frame.
    all_years = all_years.merge(data, on='Country', how='outer')

# Saving merged data to new CSV
hs_all_years = os.path.join(cwd, 'Data')
hs_all_years = os.path.join(hs_all_years, 'happiness_score_all_years.csv')
all_years.to_csv(hs_all_years, encoding='utf-8', index=False)

# Calculate mean, median, and standard deviation for all years happiness.
mean_row = {'Statistics': 'Mean'}
median_row = {'Statistics': 'Median'}
std_row = {'Statistics': 'Standard Deviation'}
for year in range(2015, 2023):
    mean = all_years[str(year)].mean()
    mean_row[str(year)] = mean
    median = all_years[str(year)].median()
    median_row[str(year)] = median
    std_deviation = all_years[str(year)].std()
    std_row[str(year)] = std_deviation

# Making a new pd data frame to be able to append.
statistics = pd.DataFrame()
statistics = statistics._append(mean_row, ignore_index=True)
statistics = statistics._append(median_row, ignore_index=True)
statistics = statistics._append(std_row, ignore_index=True)

# Saving merged data to new CSV
stats_file = os.path.join(cwd, 'Data')
stats_file = os.path.join(stats_file, 'global_statistics_all_years.csv')
statistics.to_csv(stats_file, encoding='utf-8', index=False)

### Visual representations ###
# Create a box plot of the data by years
all_years.boxplot(figsize=(10, 6))
plt.xticks(rotation=90)
plt.title(f'Box Plot of Happiness Score by Years')
plt.suptitle('')
plt.show()

# Create a line graph of each country by years
# Set the 'Country' column as the index for the DataFrame
all_years.set_index('Country', inplace=True)

# Transpose the DataFrame to have years as columns
all_years = all_years[0:10]
all_years = all_years.T
all_years = all_years[1:]

plt.figure(figsize=(12, 6))
for country in all_years.columns:
    plt.plot(all_years.index, all_years[country], label=country)

plt.title("Happiness Scores Over the Years (2015-2022)")
plt.xlabel("Year")
plt.ylabel("Happiness Score")
plt.legend()
plt.grid(True)
plt.show()