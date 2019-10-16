#!/bin/bash  
echo "This is a shell script"
#mkdir /home/sai/Documents/sai/deep-learning-face-detection/new_folder
#scp -r /home/sai/Downloads/svm.png saiamrit@ada.iiit.ac.in:/home/saiamrit/ECCV2018-FaceDeSpoofing1/data
python capture.py
python df.py --input output/output.avi --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel
sshpass -p "sgdmomentum" scp -r /home/sai/Documents/sai/deep-learning-face-detection/output saiamrit@ada.iiit.ac.in:/home/saiamrit/ECCV2018-FaceDeSpoofing1/data/real/rl
# scp -r /home/sai/Documents/sai/deep-learning-face-detection/output.txt saiamrit@ada.iiit.ac.in:/home/saiamrit/ECCV2018-FaceDeSpoofing1/data/real/rl
echo "Done"