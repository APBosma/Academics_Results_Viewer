import pandas as pd

def get_results_queries(conference, compType, compNumber, competition):
    """
    Queries the result csv files to get the corresponding results.

    Args:
        conference (str): The conference to filter by (e.g., '1A', '2A', etc.)
        compType (str): The competition type to filter by (e.g., 'Region', 'District', etc.)
        compNumber (str): The competition number to filter by (Region # or district #, else -1)
        competition (int): The competition to filter by

    Returns:
        list: Returns a dataframe of the results queries filtered by the input parameters
    """
    # Grab the csv file
    if compType == "Region":
        df = pd.read_csv(f'Results_{conference}/Results_{conference}_{compNumber}R.csv')
    elif compType == "District":
        df = pd.read_csv(f'Results_{conference}/Results_{conference}_{compNumber}D.csv')
    else:
        df = pd.read_csv(f'Results_{conference}/Results_{conference}_State.csv')

    # Filter the DataFrame based on the input parameters
    df = df[(df['Contest_ID'] == competition)]

    # Return only the columns that have at least one non-null value
    return df.dropna(axis = 1, how = 'all')

print(get_results_queries("1A", "District", "1", 12))