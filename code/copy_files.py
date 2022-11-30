import csv
import shutil
import os
with open('test.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
      # Assuming the columns in the CSV file we want are the first two  // Changed
      filename_mp3 = row[0]
      filepath_mp3 = "../mp3/"  # Changed

      new_filename_mp3 = os.path.join("../input/mp3/", filename_mp3)

      print('Copying' + filepath_mp3 + ' to ' + new_filename_mp3 + ' ...')  #Changed
      shutil.copy(filepath_mp3+filename_mp3, new_filename_mp3)   #Changed

      filename_txt = row[1]
      filepath_txt = "../txt/"  # Changed

      new_filename_txt = os.path.join("../input/txt_again/", filename_txt)

      print('Copying' + filepath_txt + ' to ' + new_filename_txt + ' ...')  #Changed
      shutil.copy(filepath_txt+filename_txt, new_filename_txt)   #Changed
      print("done")
print('All done!')