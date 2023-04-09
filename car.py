import cv2
import easyocr
import random
import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


def Start():
    m = window()
    m.show()
    return m



class window(QMainWindow):
     def __init__(self):
          super(window,self).__init__()
          self.setGeometry(0,0,400,100)
          self.setWindowTitle("Number Plate Checker")
          self.flag=True
          self.numberplate=""
          self.mydb = mysql.connector.connect(
          host='localhost',
          user="root",
          password="Ansh15O3",
          database="carplate"
          )
          self.btn1()
          
     

     def btn1(self):
          btn=QPushButton("Camera",self)
          btn2=QPushButton("Click image",self)
          btn3=QPushButton("Close camera",self)
          btn4=QPushButton("Upload Image",self)
          btn5=QPushButton("Show Registration No.",self)
          btn6=QPushButton("Add Data",self)
          btn2.move(150,0)
          btn3.move(300,0)
          btn4.move(0,50)
          btn5.move(125,50)
          btn6.move(300,50)
          btn5.resize(150,30)
          btn.resize(btn.minimumSizeHint())
          self.show()
          btn.clicked.connect(self.on_click)
          btn2.clicked.connect(self.on_click1)
          btn3.clicked.connect(self.on_click2)
          btn4.clicked.connect(self.uploadCheck)
          btn5.clicked.connect(self.showmsg)
          btn6.clicked.connect(self.add_data)

     

     def on_click(self):
          global num
          num = random.random()
          harcascade="carplate.xml"
          print("app")
          self.flag=True
          vid = cv2.VideoCapture(0)
          min_area=500
          count=0
          while(self.flag):
                
              # Capture the video frame
              # by frame
              ret, frame = vid.read()
              plate_cascade = cv2.CascadeClassifier(harcascade)
              img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          
              plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
          
              for (x,y,w,h) in plates:
                  area = w * h
          
                  if area > min_area:
                          cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                          cv2.putText(frame, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                          global img_roi
                          img_roi = cv2.convertScaleAbs(frame[y: y+h, x:x+w], alpha=1, beta=20)
                          cv2.imshow("Number plate", img_roi)
          
            
              # Display the resulting frame
              cv2.imshow('frame', frame)  
              cv2.waitKey(1)          
          
          # After the loop release the cap object
          vid.release()
          # Destroy all the windows
          cv2.destroyAllWindows()
     def on_click1(self):
          
          cv2.imwrite("scaned_img_" + str(num) + ".jpg", img_roi)
          cv2.imshow("Results",img_roi)
          cv2.waitKey(500) 
          global image_path
          image_path="scaned_img_" + str(num) + ".jpg"
          reader = easyocr.Reader(['en'],gpu=True)
          result = reader.readtext(image_path)
          print(result)
          numberplate=""
          for item in result:
               numberplate=numberplate+item[1]+" "
          self.numberplate=numberplate
          print(self.numberplate)

     def on_click2(self):
          self.flag=False

     def uploadCheck(self):
          fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Image files (*.png *.jpg *.jpeg *.bmp *.gif)")
          print(fname)
          if(fname[0]==''):
               return
          frame=cv2.imread(fname[0])
          harcascade="carplate.xml"
          plate_cascade = cv2.CascadeClassifier(harcascade)
          img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
          print(plates)
          for (x,y,w,h) in plates:
                  area = w * h
          if(len(plates)==0):
               img_roi=frame
          else:
               img_roi = frame[y: y+h, x:x+w]
          img_roi = cv2.convertScaleAbs(frame[y: y+h, x:x+w], alpha=1, beta=20)
          reader = easyocr.Reader(['en'],gpu=True)
          result = reader.readtext(img_roi)
          print(result)
          
          numberplate=""
          for item in result:
               numberplate=numberplate+item[1]+" "
          
          self.numberplate=numberplate
          print(numberplate)
        
     def showmsg(self):
          msg = QMessageBox()
          msg.setText(self.numberplate)
          retval = msg.exec_()
     
     def add_data(self):
          if(self.numberplate==""):
               print(1)
          else:
               mycursor = self.mydb.cursor()
               sql = "INSERT INTO numberplate VALUES (%s)"
               val=[self.numberplate]
               mycursor.execute(sql,val)
               self.mydb.commit()
               msg = QMessageBox()
               msg.setText("Data added")
               retval = msg.exec_()

          

     
app=QApplication(sys.argv)
gui=Start()
app.exec_()
print(gui.numberplate)



