import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import style
from PIL import Image #used for uploading image


con=sqlite3.connect("products.db")
cur=con.cursor()

defaultImg="store.png"

class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())  # after using this, we now cannot resize our window

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.addProductImg=QLabel()
        self.img=QPixmap('icons/addproduct.png')
        self.addProductImg.setPixmap(self.img)
        self.titleText=QLabel("Add Product")

        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Name of Product")
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setPlaceholderText("Enter Name of Manufacturer")
        self.priceEntry = QLineEdit()
        self.priceEntry.setPlaceholderText("Enter Price of Product")
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setPlaceholderText("Enter Quota of Product")
        self.uploadBtn=QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addProduct)

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame() #Just like group box
        self.topFrame.setStyleSheet(style.addProductTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.addProductBottomFrame())

        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price: "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Quota: "), self.quotaEntry)
        self.bottomLayout.addRow(QLabel("Upload: "), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global defaultImg
        size=(256,256)
        self.filename,ok = QFileDialog.getOpenFileName(self,"Upload Image","","Image Files (*.jpg *.png)")
        if ok:
            defaultImg = os.path.basename(self.filename)
            img=Image.open(self.filename)
            img=img.resize(size)
            img.save("img/{0}".format(defaultImg))

    def addProduct(self):
        global defaultImg
        name=self.nameEntry.text()
        manufacturer=self.manufacturerEntry.text()
        price=self.priceEntry.text()
        quota=self.quotaEntry.text()

        if(name and manufacturer and price and quota !=""):
            try:
                query="INSERT INTO 'products' (product_name, product_manufacturer,product_price,product_quota, product_img) VALUES(?,?,?,?,?)"
                cur.execute(query,(name,manufacturer,price,quota,defaultImg))
                con.commit()
                QMessageBox.information(self,"Info","Product has been added")
            except:
                QMessageBox.information(self,"Info","Product has not been added")

        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")
