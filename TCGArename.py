# -*- coding: utf-8 -*-
import os, dicom, shutil, time, dicomname, scipy

BTdict = dicomname.BTdict

start = time.time()
n, total, no_file_list = 0, 0, []
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

no_file = 0
root_path = os.path.abspath('.')
os.mkdir('new_dir')

os.chdir('DOI')
for PtIDs in os.listdir('.'):
    os.chdir(PtIDs)
    os.mkdir(root_path + "/new_dir/" + PtIDs[5:12])
    nonsense_dir_name = os.listdir('.')
    for StudyList in nonsense_dir_name:
        os.chdir(StudyList)
        sequence_counter = []
        for sequence_name in os.listdir('.'):
            os.chdir(sequence_name)
            try:
                for file_name in os.listdir('.'):
                    ds = dicom.read_file(file_name)
                    try:
                        sequence_name = BTdict[ds.SeriesDescription]
                    except:
                        sequence_name = 'NoName'
                    if sequence_name in sequence_counter:
                        sequence_name = sequence_name + "_" + str(sequence_counter.count(sequence_name))
                    sequence_counter.append(sequence_name)
                    try:
                        os.mkdir(root_path + "/new_dir/" + PtIDs[5:12] + "/" + sequence_name)
                    except:
                        pass
                    save_name = (PtIDs[5:12] + "/" + sequence_name + "/"
                                + sequence_name + "_" + file_name[3:])
                    save_name = (root_path + "/new_dir/" + save_name)
                    shutil.copy(file_name, save_name)
                    n += 1
                    if scipy.sqrt(n/10) == int(scipy.sqrt(n/10)):
                        elapsed_time = time.time() - start
                        print("{0}/{1}, {2:2.02f}% of cases copied,  elapsed time: {3:2.02f} sec".format(n, total, (n/total)*100, elapsed_time))
                        print("{0:2.02f} sec to finish copying".format(((elapsed_time/n)*total)-elapsed_time))
                        print(' ')
            except:
                print('file がありませんでした。')
                no_file_list.append(os.path.abspath('.'))
                no_file += 1
            os.chdir('..')
        os.chdir('..')
    os.chdir('..')

print("{0:02.2f}% のフォルダーで、dicom ファイルが見つかりませんでした".format((no_file / total)*100))
print(no_file_list)
print("以上のフォルダーで、dicomファイルが見つかりませんでした")
print("終了します")
