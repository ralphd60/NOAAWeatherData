# receives a label and then counts that label
def type_count (row, col,  counts_dict2):
    '''this function will take a column, and groups by event type'''
    event_name = row[col]

    if event_name == 'Hurricane (Typhoon)':
        event_name = 'Hurricane'
        print(event_name)
    if event_name in counts_dict2.keys():
        counts_dict2[event_name] += 1
    else:
        counts_dict2[event_name] = 1

    return counts_dict2