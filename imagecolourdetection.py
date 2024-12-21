
import cv2
import pandas as pd

# Prompting the user to enter the image name
img_name = input("Enter the image file name (with extension, e.g., 'image1.jpg'): ")

# Reading the image with OpenCV
img = cv2.imread(img_name)

if img is None:
    print(f"Error: Could not load the image '{img_name}'. Please check the file name and try again.")
    exit()

# Declaring global variables
r = g = b = xpos = ypos = 0

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

# Function to track mouse movement and get the color at the cursor position
def draw_function(event, x, y, flags, param):
    global xpos, ypos, r, g, b
    if event == cv2.EVENT_MOUSEMOVE:  # Triggered whenever the mouse moves
        xpos, ypos = x, y
        if xpos < img.shape[1] and ypos < img.shape[0]:
            b, g, r = img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
    # Create a copy of the image to draw the rectangle and text
    img_copy = img.copy()

    # Draw rectangle and display color name and RGB values
    cv2.rectangle(img_copy, (20, 20), (750, 60), (b, g, r), -1)
    text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
    cv2.putText(img_copy, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # For very light colors, display text in black
    if r + g + b >= 600:
        cv2.putText(img_copy, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # Show the image with color name displayed dynamically
    cv2.imshow("image", img_copy)

    # Break the loop when user hits the 'Esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

