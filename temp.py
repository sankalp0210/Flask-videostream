import subprocess
bashCommand = "sshpass -p \"Fingerface!\" ssh biometrics@cvit.iiit.ac.in \"touch b.txt\""
output = subprocess.check_output(['bash','-c', bashCommand])