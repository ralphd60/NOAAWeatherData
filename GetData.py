import requests
from bs4 import BeautifulSoup


def get_file_list(archive_url):
    """using the request module, this will retrieve a sudo html list of the files in the director
    it will then use the Beautiful soup module to format the returned data into better formed html
    thrn filter snd return the file  list."""

    # create response object
    r = requests.get(archive_url)

    # create beautiful-soup object
    soup = BeautifulSoup(r.content, "html.parser")

    # find all files in the directory using the tag <a>
    links = soup.findAll('a')

    # filter the link sending with .gz
    file_list = [archive_url + link['href'] for link in links if link['href'].endswith('gz')]

    return file_list


def retrieve_and_filter(detail_data, dest_dir, url):
    # use a list comprehension to filter the list for just specific files
    file_list_filtered = [x for x in detail_data if 'StormEvents_details' in x]
    # debug print statements
    # print(file_list_filtered)
    # print(len(file_list_filtered))

    for link in file_list_filtered:
        # splicing the file to just capture the name
        filename = link.split('/')[-1]
        # then finally retrieving the file
        response = requests.get(url + filename)
        # debug print statemnet

        if response.status_code == 200:
            with open(dest_dir + filename, 'wb') as f:
                # Chunking it seems to create problems ith a gzip file
                # for chunk in response.iter_content(chunk_size = 1024*1024):
                # write the file out to local directory
                f.write(response.content)