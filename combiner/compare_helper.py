import pandas as pd


# compare given two lists
def compare_two_lists(list_one, list_two):
    return list_one == list_two


def to_data_frame(header, filename):
    master_lists = header
    master_lists = [item for newlist in master_lists for item in newlist]
    master_frame = pd.DataFrame(master_lists)
    return master_frame


def flatern_to_list(master_lits):
    return [item for newlist in master_lits for item in newlist]


def check_header_counts(project_file, user_file):
    return len(project_file) == len(user_file)


def show_columns_difference(project_file, user_file):

    loop = project_file if len(project_file) > len(user_file) else user_file

    for index, column in enumerate(loop):

        try:
            user_column = user_file[index]
            project_column = project_file[index]

            if project_column == user_column:
                print(f"{project_column:<15} | {user_column:<15}")

            else:
                print(f"{project_column:<15} | {user_column:<15}  <-- Different")

        except IndexError:
            if len(project_file) > len(user_file):
                print(
                    f"{project_column:<15} | \033[91m{"Missing"}\033[0m"
                )
            elif len(project_file) < len(user_file):
                print(
                    f"\033[91m{"Extra":<15}\033[0m | {user_column}"
                )
