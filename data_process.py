import os
import pandas as pd
import pycountry

def get_country_code(country_name):
    try:
        # Look up country by name
        return pycountry.countries.get(name=country_name).alpha_2
    except AttributeError:
        # Return None if country name not found
        return None

def add_country_code_column():
    # Get data file directory
    cwd = os.getcwd()
    original_data_path = cwd + '/original_data/'
    processed_data_path = cwd + '/processed_data/'
    
    # Get all files in the specified directory
    file_names = os.listdir(original_data_path)

    # Iterate through all files in the directory
    for file_name in file_names:

        # Skip the file if it is not a CSV file
        if not file_name.endswith('.csv'):
            continue

        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(original_data_path + file_name, encoding='utf-8')

        # Create a new column 'country_code' by mapping the country name to its code
        df['country_code'] = df['country_name'].apply(get_country_code)

        # Save the modified DataFrame back to a new CSV file
        df.to_csv(processed_data_path + file_name, index=False, encoding='utf-8')


def join_tables():
    # Get data file directory
    cwd = os.getcwd()
    processed_data_path = cwd + '/processed_data/'

    # Get all files in the specified directory
    file_names = os.listdir(processed_data_path)

    # Extract country names and their alpha-2 codes
    countries_data = [{'country_name': country.name, 'country_code': country.alpha_2} for country in pycountry.countries]

    # Iterate through all files in the directory and join tables
    joined_df = pd.DataFrame(countries_data)

    for file_name in file_names:

        # Skip the file if it is not a CSV file
        if not file_name.endswith('.csv'):
            continue

        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(processed_data_path + file_name, encoding='utf-8')

        # Drop duplicate columns
        columns_to_drop = [col for col in df.columns if col in joined_df.columns and col != 'country_code']
        df.drop(columns_to_drop, axis=1, errors='ignore', inplace=True)
        df.dropna(subset=['country_code'], inplace=True)

        # Join tables with country_code as key
        joined_df = joined_df.merge(df, on='country_code', how='outer')

    # Drop unnecessary columns if they exist
    columns_to_drop = ['slug', 'date_of_information', 'ranking', 'country_code_y', 'RANK']
    joined_df.drop(columns_to_drop, axis=1, errors='ignore', inplace=True)

    # Save the resulting DataFrame to a new CSV file
    joined_df.to_csv(os.path.join(processed_data_path, 'master_data_2022.csv'), encoding='utf-8', index=False)


def main():

    # Add 'country_code' column to the original data
    add_country_code_column()

    # Join tables to get the dataset we need for analysis
    join_tables()


if __name__ == '__main__':
    main()