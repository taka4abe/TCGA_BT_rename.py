# -*- coding: utf-8 -*-
import os, dicom, shutil, time, dicomname

print('')
print('code started...')
print('')
BTdict = dicomname.BTdict

start = time.time()
n, total, no_file_list, no_InstanceNo= 0, 0, [], []
target_dir = '.'

for root, dirs, files in os.walk(target_dir):
    for file_name in files:
        try:
            file_name_, ext = os.path.splitext(file_name)
            if ext == '.dcm':
                total += 1
            else:
                pass
        except:
            pass

print('total of {} dicom files'.format(total))
print('')

no_file = 0
root_path = os.path.abspath('.')
os.mkdir('renamed')
print("os.mkdir('renamed')")

os.chdir('DOI')
for PtIDs in os.listdir('.'):
    os.chdir(PtIDs)
    os.mkdir(root_path + "/renamed/" + PtIDs[5:12])
    nonsense_dir_name = os.listdir('.')
    for StudyList in nonsense_dir_name:
        os.chdir(StudyList)
        sequence_counter = []
        for sequence_name in os.listdir('.'):
            os.chdir(sequence_name)
            try:
                ds = dicom.read_file('000000.dcm')
                try:
                    sequence_name = BTdict[ds.SeriesDescription]
                except:
                    sequence_name = 'NoName'
                sequence_counter.append(sequence_name)
                path_count = sequence_counter.count(sequence_name)
                sequence_name = sequence_name + "_{0:02d}".format(path_count)
                save_path = root_path + "/renamed/" + PtIDs[5:12] + "/" + sequence_name
                try:
                    os.mkdir(save_path)
                except:
                    pass
                dsNo = 0
                for file_name in os.listdir('.'):
                    ds = dicom.read_file(file_name)
                    try:
                        dsNo = int(ds.InstanceNumber)
                    except:
                        dsNo += 1
                        print("No InstanceNumber")
                        if save_path not in no_InstanceNo:
                            no_InstanceNo.append(save_path)
                        else:
                            pass
                    dsNo = "{0:04}".format(dsNo)
                    save_name = (save_path + "/" + sequence_name + "_" + dsNo + ".dcm")
                    shutil.copy(file_name, save_name)
                    n += 1
            except:
                print('No files were found')
                no_file_list.append(os.path.abspath('.'))
                no_file += 1
            os.chdir('..')
        os.chdir('..')
    elapsed_time = time.time() - start
    est_time = ((elapsed_time/n)*total)
    process_speed = n/elapsed_time
    print('')
    print('  ID:', PtIDs, 'renamed')
    print("{0}/{1} renamed, {2:1.0f} files/sec, elapsed/est: {3:2.0f}/{4:2.0f} sec".format(n, total, process_speed, elapsed_time, est_time))
    os.chdir('..')

print("couldn't find dicom files in {0:02.2f}% of dirs".format((no_file / total)*100))
print(no_file_list, "don't have any dcm file")
print("no InstanceNumber in", no_InstanceNo, "dcm files, dcm file order could be distorted.")
print("finished")
