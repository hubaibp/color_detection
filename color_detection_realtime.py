

import cv2
import pandas as pd

# Reading CSV file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to calculate the minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to capture the mouse position
def draw_function(event, x, y, flags, param):
    global xpos, ypos
    if event == cv2.EVENT_MOUSEMOVE:  # Capture position as the mouse moves
        xpos, ypos = x, y

# Initializing global variables
r = g = b = xpos = ypos = 0
previous_color = (0, 0, 0)

# Starting the webcam
cap = cv2.VideoCapture(0)

cv2.namedWindow('Real-Time Color Detection')
cv2.setMouseCallback('Real-Time Color Detection', draw_function)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get the color under the current cursor position
    if xpos < frame.shape[1] and ypos < frame.shape[0]:
        b, g, r = frame[ypos, xpos]
        b = int(b)
        g = int(g)
        r = int(r)

    # Apply smoothing to reduce fluctuations
    current_color = (r, g, b)
    if abs(r - previous_color[0]) > 5 or abs(g - previous_color[1]) > 5 or abs(b - previous_color[2]) > 5:
        previous_color = current_color
    else:
        r, g, b = previous_color

    # Drawing a rectangle for the color display
    cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)

    # Creating text string to display (Color name and RGB values)
    text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

    # Displaying the text on the rectangle
    cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # For very light colors, display text in black
    if r + g + b >= 600:
        cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # Showing the video feed
    cv2.imshow("Real-Time Color Detection", frame)

    # Breaking the loop when the user hits the 'Esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Releasing the camera and closing all OpenCV windows
cap.release()
cv2.destroyAllWindows()
