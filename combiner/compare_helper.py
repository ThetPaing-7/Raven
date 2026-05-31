import pandas as pd


# compare given two lists
def compare_two_lists(list_one, list_two):
    return list_one == list_two



def to_data_frame(header, filename):
    master_lists = header
    master_lists = [item for newlist in master_lists for item in newlist ]
    master_frame = pd.DataFrame(master_lists)
    master_frame["filename"] = filename
    return master_frame