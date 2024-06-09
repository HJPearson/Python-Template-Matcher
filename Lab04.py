import cv2


# Callback for selecting the template coordinates
def mouse_callback(event, x, y, flags, param):
    global coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates.append(x)
        coordinates.append(y)

coordinates = []

# Open the video file
vc = cv2.VideoCapture('building.avi')

if not vc.isOpened():
    print("Error opening video.")

# Get the number of frames in the video
nFrames = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))

# Read the first frame and convert it to grayscale
ret, frame = vc.read()

# Convert the image to grayscale
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Display the first frame and let user choose template location
cv2.imshow('User Input', frame)
cv2.setMouseCallback('User Input', mouse_callback)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Set the coordinates that the user chose
x = coordinates[0]
y = coordinates[1]

# I have found the most success by using M = 8
M = 8

# Draw a red rectangle around the chosen point (rectangle template)
cv2.rectangle(frame, (x - 10, y - 10), (x + 10, y + 10), (255, 0, 0), 2)
T = frame[y-M:y+M, x-M:x+M]

# The size of the template
w, h = T.shape[::-1]

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

for i in range(nFrames-1):
    ret, frame = vc.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(frame, T, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
    cv2.putText(frame, "Minimum value: {}, Maximum value: {}".format(min_val, max_val), (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    cv2.imshow('Result', frame)
    output.write(frame)
    cv2.imshow('Result', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vc.release()
output.release()
cv2.destroyAllWindows()
