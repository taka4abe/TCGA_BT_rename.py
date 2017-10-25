# -*- coding: utf-8 -*-
import argparse, os, dicom, shutil, time, dicomrename
parser = argparse.ArgumentParser(description='''This code modifies and
    organizes the name of the directory tree which contains dcm files.
    To use this code, please save the file named "ser_description_dict"
    which has dictionary to organize the sequence name in the current
    working directory. To create this dictionary, another repository
    "get_dcm_series_description.py" would be helpful.''')
parser.add_argument("-indir", nargs= 1, help=""": the name of the root of
                    the dir_tree where dicom datas are, default: '.'  """)
parser.add_argument("-outfile", nargs= 1, help=": name of file to save the list.  ")
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1, Oct/21/2017')
args = parser.parse_args()
try:
    in_dir = args.indir[0]
except:
    in_dir = '.' # defaul target directory
try:
    out_dir = args.outfile[0]
except:
    out_dir = "renamed"
    pass

print("in_dir: " + in_dir + "\nout_dir: " + out_dir + "\ncode started...\n")
dcm_dict = dicomname.BTdict

start = time.time()
n, total = 0, 0

for root, dirs, files in os.walk(in_dir):
    for file_name in files:
        total += 1

print('total of {} dicom files\n'.format(total))

root_path = os.path.abspath('.')
os.mkdir('renamed')
print("os.mkdir('renamed')")
no_file, no_file_list = 0, []
no_InstanceNo = []

for PtIDs in os.listdir('.'):
    if os.path.isdir(PtIDs):
        os.chdir(PtIDs)
        for StudyList in os.listdir('.'):
            if os.path.isdir(StudyList):
                os.chdir(StudyList)
                sequence_counter = []
                for sequence_name in os.listdir('.'):
                    if os.path.isdir(sequence_name):
                        os.chdir(sequence_name)
                        try:
                            ds = dicom.read_file('im0')
                            try:
                                sequence_name = dcm_dict[ds.SeriesDescription]
                            except:
                                sequence_name = 'NoName'
                            sequence_counter.append(sequence_name)
                            path_count = sequence_counter.count(sequence_name)
                            sequence_name = sequence_name + "_{0:02d}".format(path_count)
                            save_path = root_path + "/renamed/" + PtIDs + "/" + sequence_name
                            try:
                                os.makedirs(save_path)
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
                                save_name = (save_path + "/" + PtIDs + "_" + sequence_name + "_" + dsNo + ".dcm")
                                shutil.copy(file_name, save_name)
                                n += 1
                        except:
                            print('No dicom files were found')
                            no_file_list.append(os.path.abspath('.'))
                            no_file += 1
                        os.chdir('..')
                    else:
                        pass
                os.chdir('..')
            else:
                pass
        os.chdir('..')
    else:
        pass
    elapsed_time = time.time() - start
    est_total = ((elapsed_time/n)*total)
    process_speed = n/elapsed_time
    print('')
    print('  ID: {0} was renamed, {1:1.0f} files/sec'.format(PtIDs, process_speed))
    if est_total < 600:
        print("{0}/{1} renamed, elapsed/est_total: {2:2.0f}/{3:2.0f} sec".format(n, total, elapsed_time, est_total))
    elif est_total < 4800:
        print("{0}/{1} renamed, elapsed/est_total: {2}/{3} min".format(n, total, elapsed_time//60, est_total//60))
    else:
        print("{0}/{1} renamed, elapsed/est_total: {2:2.1f}/{3:2.1f} min".format(n, total, elapsed_time/3600, est_total/3600))

print("couldn't find dicom files in {0:02.2f}% of dirs".format((no_file / total)*100))
print(no_file_list, "don't have any dcm file")
print("no InstanceNumber in", no_InstanceNo, "dcm files, dcm file order could be distorted.")
print("finished")
