import os
import glob
import shutil
import csv

true_path =   '../input/txt' + '/*.txt'
pred_path = '../output_txt' + '/*.txt'

# files_name = os.path.basename('../output_txt')
names = [os.path.basename(x) for x in glob.glob('../input/mp3'+ '/*')]
with open('test.csv', 'r') as f:
    reader = csv.reader(f)
    list2 = [row.split(',')[0] for row in f]
    # print(list2)
    for name in names:
        if name not in list2:
            print(name)
    # for row in reader:
    #     filename_txt = row[0]
    #     if filename_txt in names:
    #         print(filename_txt)
            
            # filepath_mp3 = "../txt/"  # Changed

            # new_filename_mp3 = os.path.join("../input/txt/", name)

            # print('Copying' + filepath_mp3 + ' to ' + new_filename_mp3 + ' ...')  #Changed
            # shutil.copy(filepath_mp3+name, new_filename_mp3)   #Changed


# for path in pred_:
#     shutil.copyfile(path, true_path)

