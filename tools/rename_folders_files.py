import os

cwd = os.getcwd()
# test_folder_dir = f'{cwd}\\tools\\testfolder'
test_folder_dir = os.path.join(cwd, 'tools', 'testfolder')

# # Alternative way to get folders
# walk = os.walk(test_folder_dir)
# dirs = [x[0].split('\\')[9:] for x in walk]

# Rename train folders
dataset_dir = os.path.join(cwd, 'resources', 'data',
                           'growth_pred_Dataset1_and_2')
train_dir = os.path.join(dataset_dir, 'train')
train_folders = os.listdir(train_dir)

for i, folder in enumerate(train_folders):
    current_path = os.path.join(train_dir, folder)
    folder_nr = int(folder[-2:])
    folder_nr_new = folder_nr + 90
    new_folder_name = f'{folder[:-2]}{folder_nr_new}'
    new_path = os.path.join(train_dir, new_folder_name)
    print(folder)
    # print(new_folder_name)
    # print(current_path)
    # print(new_path)
    # os.rename(current_path, new_path)


# Rename test folders
test_dir = os.path.join(dataset_dir, 'test')
test_folders = os.listdir(test_dir)

for i, folder in enumerate(test_folders):
    current_path = os.path.join(test_dir, folder)
    folder_nr = int(folder[-2:])
    folder_nr_new = folder_nr + 10
    new_folder_name = f'{folder[:-2]}{folder_nr_new}'
    new_path = os.path.join(test_dir, new_folder_name)
    print(folder)
    # print(new_folder_name)
    # print(current_path)
    # print(new_path)
    # os.rename(current_path, new_path)
