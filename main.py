import pandas as pd
import glob
import os.path
import gzip
import numpy as np
from GetData import *

from AnalysisType import *
import matplotlib.pyplot as plt


def count_entries(csv_file, c_size, delimit, colname1):
    """Return a dictionary with counts of or totals of a second column
    occurrences as value for each key."""

    # Initialize an empty dictionary: counts_dict
    source_dir = csv_file
    dest_dir = csv_file

    counts_dict = {}
    episode_list = []
    year_list = []
    group_dict = {}
    # allFiles = glob.glob(csv_file + "*.csv")

    c = None  # this is used to remove the header in files of more then one.

    for src_name in glob.glob(os.path.join(source_dir, '*.gz')):
        base = os.path.basename(src_name)
        dest_name = os.path.join(dest_dir, base[:-3])

        # using context manager, uncompressing the file then writing out the csv
        with gzip.open(src_name, 'rb') as infile:
            with open(dest_name, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)
                outfile.write(line)
        # for debug - print out the csv file name
        # Iterate over the file chunk by chunk
        for chunk in pd.read_csv(dest_name, delimit, chunksize=c_size, skiprows=c):
            # Iterate over the rows in DataFrame - i think this can be simplified using posibly groupby method
            for lab, row in chunk.iterrows():  # lab is really the index number, not used
                if row['EVENT_TYPE'] == 'Hurricane' or row["EVENT_TYPE"] == 'Tropical Storm' \
                  or row["EVENT_TYPE"] == 'Tornado' or row["EVENT_TYPE"] == 'Hurricane (Typhoon)':
                    if row['YEAR'] not in year_list:
                        year_list.append((row['YEAR']))
                        counts_dict = {}
                    if np.isnan(row['EPISODE_ID']):
                        episode = row['EVENT_ID']
                    else:
                        episode = row['EPISODE_ID']
                    if (str(episode) + str(row['EVENT_TYPE'])) not in episode_list:
                        episode_list.append(str(episode) + str(row['EVENT_TYPE']))
                        counts_dict = type_count(row, colname1, counts_dict)

        if year_list[-1] not in group_dict:
            group_dict[year_list[-1]] = counts_dict
        else:
            group_dict.update({year_list[-1]: counts_dict})

        # this is to make sure the header is not retrieved for all subsequent files
        if c is None:
            c == None
        os.remove(dest_name)

    return group_dict


if __name__ == '__main__':
    url = 'https://www1.ncdc.noaa.gov/pub/data/swdi/stormevents/csvfiles/'

    dir_dest = 'C:\\Development\\data\\'

    # Get the list of files in the directory (this calls the function get_file_list()
    # passing the url of the directory where the file is located
    # data_detail = get_file_list(url)
    # retrieve_and_filter(data_detail, dir_dest, url)

    # calls the function thar will uncompress files, load into datadframe and then
    # scrub scrub the data
    result_counts = \
        count_entries('C:\\Development\\data\\', 10000, ',', 'EVENT_TYPE')

    # Print result_counts
    print(result_counts)
    df_temp = pd.DataFrame(result_counts)
    df = df_temp.transpose()
    print(df.head(10))

    df.plot(kind="bar", log=True, stacked=False)
    # df.plot(kind="bar", stacked=True)
    plt.show()
