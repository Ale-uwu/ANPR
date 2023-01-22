# import the opencv library
import cv2

# define a video capture object
#vid = cv2.VideoCapture(0)
#camera = cv2.VideoCapture("192.168.18.30:8080/video")
cap = cv2.VideoCapture('http://192.168.18.4:8080/video')
while(True):
	
	# Capture the video frame
	# by frame
	ret, frame = cap.read()

	# Display the resulting frame
	cv2.imshow('frame', frame)
	
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
