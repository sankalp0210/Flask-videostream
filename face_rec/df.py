import numpy as np
import argparse
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.45,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
c = 0
txt_file = args["input"].split('/')[-1].split('.')[-2]
f = open("output/{}.txt".format(txt_file),"w")
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] starting video stream...")
'''vs = VideoStream(src=0).start()
time.sleep(2.0)'''
con = []
cap = cv2.VideoCapture(args["input"])

while(cap.isOpened()):
	ret,frame = cap.read()
	# loop over the frames from the video stream
	if ret == True:
		#print(c)
		c += 1
		frame = cv2.resize(frame, (900,600))
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (600, 600)), 1.0,(150, 150), (104.0, 177.0, 123.0))
		net.setInput(blob)
		detections = net.forward()
		conf = detections[0,0,:,2]
		#print("All confidences = ",conf)
		conf = sorted(conf,reverse = True)
		confi = conf[0]
		#print(confi)
		if confi < 0.5 :
			con.insert(c-1,0)
			#con[c-1] = 0
		else:
			con.insert(c-1,1)
			#con[c-1] = 1

		#print(detections.shape[2])
		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]

			if confidence < args["confidence"]:
				continue


			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

			(startX, startY, endX, endY) = box.astype("int")

			w = endX - startX
			l = endY - startY

			f.write("{} {} {} {}\n".format(startX,startY,w,l))

			#print("For "+str(i)+" the l,w are: "+str(l)+" "+str(w)+" and area is: "+str(l*w))

			text = "{:.2f}%".format(confidence * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
			#print("Hello")
			cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

		#print("Hi")
		cv2.imshow("Frame",frame)

		k = cv2.waitKey(1)
		if k == 27:
			break
	else:
		break

f.close()
cap.release()
cv2.destroyAllWindows()
