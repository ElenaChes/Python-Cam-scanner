#============================IMPORTS================================
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math 
import sys
import os
folder_path = os.getcwd()

#============================FUNCTIONS==============================
# Read input
def getFilenames():
  if len(sys.argv) < 2:
    print("Missing arguments, run this program using the following syntax:\n"+
          "\"python app.py path_input_img path_output_img\"\n"+
          "- path_input_img - path to your scanned image.\n"+
          "- path_output_img - path to save the edited image, if none is provided it'll be displayed instead.")
    exit() 
  path_input_img = sys.argv[1].replace("/", "\\")
  path_output_img = sys.argv[2].replace("/", "\\") if (len(sys.argv) >= 3) else None
  return (path_input_img,path_output_img)  

#===================================================================
# Read image and check valid path
def getImg(path_input_img):
  # using "if" instead or "try-except" because cv2.imread doesn't throw exception
  img = cv2.imread(path_input_img, cv2.IMREAD_COLOR)
  if img is None:
    print("Couldn't find an image in path: "+folder_path+"\\"+path_input_img+".")
    exit() 
  return (img)  

#===================================================================
# Replace green screen       
def processImg(img):
  # Binarization
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_gray = cv2.GaussianBlur(img_gray, (99, 99), 0)
  (T, img_bin) = cv2.threshold(img_gray, 90, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

  # Find biggest contour
  (cnts, _) = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnt = max(cnts, key=cv2.contourArea)

  # Finding corners
  epsilon = 0.1*cv2.arcLength(cnt, True)
  approx = cv2.approxPolyDP(cnt, epsilon, True)
  p1 = approx[0][0]
  p2 = approx[1][0]
  p3 = approx[2][0]
  p4 = approx[3][0]
  
  # Finding height and width 
  edge1 = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
  edge2 = math.sqrt(((p2[0] - p3[0]) ** 2) + ((p2[1] - p3[1]) ** 2))
  edge3 = math.sqrt(((p3[0] - p4[0]) ** 2) + ((p3[1] - p4[1]) ** 2))
  edge4 = math.sqrt(((p4[0] - p1[0]) ** 2) + ((p4[1] - p1[1]) ** 2))
  side1 = round(min(edge1, edge3))
  side2 = round(min(edge2, edge4))
  if side1 > side2:
    height = side1
    width = side2
    corners=[p1,p4,p2,p3]
  else:
    height = side2
    width = side1
    corners=[p2,p1,p3,p4]

  # Transformation matrix
  pts1 = np.float32(corners)
  pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
  M = cv2.getPerspectiveTransform(pts1,pts2)

  # Transform
  img_output = cv2.warpPerspective(img,M,(width,height))
  return img_output

#===================================================================
# Try to save or display
def saveImg(path_output_img,img_output):
  # if ofilename exists, tries to save
  # if ofilename wasn't given or save failed -> imshow()
  if path_output_img is not None:
    try:
      saved = cv2.imwrite(path_output_img,img_output)
      if saved:
        print("Created "+folder_path+"\\"+path_output_img+".")
        return
      print("Couldn't save the image in path: "+folder_path+"\\"+path_output_img+", displaying instead.")
    except Exception as error:
      #print (error)
      print("Couldn't save the image in path: "+folder_path+"\\"+path_output_img+", displaying instead.")
  else:
    print("Wasn't given a path for the output image, displaying instead.")
    
  # Didn't save, display image 
  plt.subplots(1,1, num="Output Image", constrained_layout=True)
  b,g,r=cv2.split(img_output)
  img = cv2.merge((r, g, b))
  plt.imshow(img) ;plt.subplot(111); plt.axis("off")
  plt.show()

#==============================MAIN=================================
def main():
  # Read input
  path_input_img,path_output_img = getFilenames()

  # Read image
  img = getImg(path_input_img)

  # Align paper
  img_output = processImg(img)

  # Try to save or display
  saveImg(path_output_img,img_output)

#===================================================================  
if __name__ == "__main__":
  main()