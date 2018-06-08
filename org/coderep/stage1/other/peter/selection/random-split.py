#encoding=utf-8

# Copyright (c) 2017 Deyatech. All rights reserved.
# Authors: Peter Podstreleny <peter.podstreleny@deyatech.com>

# random-split.py

# This script randomly splits data set into training data set and target data set.

import os
import random
import shutil

# Initialize variables
user = 'admin'
c_import_path =           'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/selection/contracts/input/'
c_export_target_path =    'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/selection/contracts/output/target/'
c_export_training_path =  'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/selection/contracts/output/training/'
n_import_path =           'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/selection/non-contracts/input/'
n_export_target_path =    'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/selection/non-contracts/output/target/'
n_export_training_path =  'c:/Users/' + user + '/Dropbox/AI Project/AI/bin/selection/non-contracts/output/training/'

c_target_documents_length = 5
n_target_documents_length = 5

c_document_set_length = 0
n_document_set_length = 0

c_random_x = []
n_random_x = []

# Set document length for both classes (contract, non-contract)
c_document_set_length = len([filename for filename in os.listdir(c_import_path) if os.path.isfile(os.path.join(c_import_path, filename))])
n_document_set_length = len([filename for filename in os.listdir(n_import_path) if os.path.isfile(os.path.join(n_import_path, filename))])

# Set random documents from both documents sets (contract, non-contract)
c_random_x = random.sample(range(0, c_document_set_length), c_target_documents_length)
n_random_x = random.sample(range(0, n_document_set_length), n_target_documents_length)

# Remove any data in output folders
paths = [c_export_target_path, c_export_training_path, n_export_target_path, n_export_training_path]

for path in paths:
    filelist = [f for f in os.listdir(path)]
    for f in filelist:
        os.remove(os.path.join(path, f))

# In contract set random split data
print('Random contract selection: ' + str(c_random_x))
for x, filename in enumerate(os.listdir(c_import_path)):
    if x in c_random_x:
        # copy to target folder
        shutil.copy2(c_import_path + filename, c_export_target_path)
        print('[***]', x, filename)
    else:
        # copy to training folder
        shutil.copy2(c_import_path + filename, c_export_training_path)
        print('[---]', x, filename)

# In non-contract set random split data
print('Random non-contract selection: ' + str(n_random_x))
for x, filename in enumerate(os.listdir(n_import_path)):
    if x in n_random_x:
        # copy to target folder
        shutil.copy2(n_import_path + filename, n_export_target_path)
        print('[***]', x, filename)
    else:
        # copy to training folder
        shutil.copy2(n_import_path + filename, n_export_training_path)
        print('[---]', x, filename)
