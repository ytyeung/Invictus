import subprocess
RECOG_ID=subprocess.Popen('julius -input rawfile -quiet -C /home/pi/julius4/Invictus.jconf -outfile |bg',shell=True)
RECOG_ID.communicate('/home/pi/julius4/rec.wav')          