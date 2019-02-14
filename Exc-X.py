import requests
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtGui, QtCore, QtWebEngineWidgets
import sys
from requests.exceptions import ConnectionError
import datetime
import sqlite3

# author : ethemguener@gmail.com

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.setWindowTitle("Exc-X")
            
    def init_ui(self):
        
        ### Creating database and tables for hold data which come from user and stock market.
        self.conn = sqlite3.connect("currency_Database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS account (usd INT, eur INT, try INT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS myAccount (usd INT, eur INT, try INT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (datetime TEXT, soldMoney INT, boughtMoney INT, fee INT, currencyVal INT)")
        self.cursor.execute("INSERT INTO myAccount VALUES(?,?,?)",(0,0,0))
        self.cursor.execute("INSERT INTO account VALUES(?,?,?)",(150000,150000,300000))
        self.conn.commit()
        
        self.msgBox = QtWidgets.QMessageBox()   ## For errors.
        self.setWindowIcon(QtGui.QIcon('myIcon.png'))   ## Icon setting.
        
        try:
            
            ## A timer for refresh the application and a label for give time information.
            self.clockLabel = QtWidgets.QLabel("")
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.showTime) ## going to a function.
            self.timer.start(30000)
            
            ## Scraping data.
            page = requests.get('https://www.bloomberght.com')
            soup = BeautifulSoup(page.content, 'html.parser')
            currency = soup.find(class_='col-md-10 col-sm-12 col-xs-12 marketsWrap')
            currency_dolar = currency.find(id = "dolar")
            currency_euro = currency.find(id = "euro")
            currency_euro_usd = currency.find(id="eur-usd")
            currency_value_eurusd = currency_euro_usd.select(".LastPrice")
            currency_value_dolar = currency_dolar.select(".LastPrice")
            currency_value_euro = currency_euro.select(".LastPrice")
            getting_closer = currency.find_all(class_="marketsCol")
            
            ## These try, except blocks are controlling percental change color. It was a big problem. When the percental change color change, I get an AttributeError.
            ## Because data comes from another class. With try-except blokcs, every situation is under control.
            try:
                self.usd_try_percantal_ratio = getting_closer[1].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.usd_try_percantal_ratio = getting_closer[1].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.usd_try_percantal_ratio = "0.00"
                
            try:
                self.euro_try_percantal_ratio = getting_closer[2].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_try_percantal_ratio = getting_closer[2].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_try_percantal_ratio = "0.00"
    
            try:
                self.euro_usd_percantal_ratio = getting_closer[3].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_usd_percantal_ratio = getting_closer[3].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_usd_percantal_ratio = "0.00"
            
            ## Table settings. There are 4 table. Currency information will insert these tables. There is
            ## percental change table. Also, there are two table sell and buy for giving the user
            ## real values about currency.
            self.currency_table = QtWidgets.QTableWidget()
            self.currency_table.setRowCount(3)
            self.currency_table.setColumnCount(2)
            self.currency_table.setColumnWidth(0,152)
                
            self.currency_ratio_table = QtWidgets.QTableWidget()
            self.currency_ratio_table.setRowCount(3)
            self.currency_ratio_table.setColumnCount(2)
            self.currency_ratio_table.setColumnWidth(0,152)
            
            self.myCurrency_table_buy = QtWidgets.QTableWidget()
            self.myCurrency_table_buy.setRowCount(2)
            self.myCurrency_table_buy.setColumnCount(2)
            self.myCurrency_table_buy.setColumnWidth(0,152)

            self.myCurrency_table_sell = QtWidgets.QTableWidget()
            self.myCurrency_table_sell.setRowCount(2)
            self.myCurrency_table_sell.setColumnCount(2)
            self.myCurrency_table_sell.setColumnWidth(0,152)
            
            ## Temprorary variable for currency values. First we have to clear the html codes with get_text()
            self.temp_value1 = currency_value_dolar[0].get_text()
            self.temp_value2 = currency_value_euro[0].get_text()
            self.temp_value3 = currency_value_eurusd[0].get_text()
            
            ## And then we have to replace ',' to '.' because as you know, we cannot use numbers in Python like 5,9.
            self.value1 = self.temp_value1.replace(',','.')
            self.value2 = self.temp_value2.replace(',','.')
            self.value3 = self.temp_value3.replace(',','.')
            
            ## We insert data into the tables.
            
            ## exchange values -->>>
            self.currency_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.value1))
            
            self.currency_table.setItem(1,0, QtWidgets.QTableWidgetItem("EUR/TRY"))
            self.currency_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.value2))
            
            self.currency_table.setItem(2,0, QtWidgets.QTableWidgetItem("EUR/USD"))
            self.currency_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.value3))
            
            ## percantal ratios -->>
            self.currency_ratio_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_ratio_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.usd_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(1,0, QtWidgets.QTableWidgetItem("EURO/TRY"))
            self.currency_ratio_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.euro_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(2,0, QtWidgets.QTableWidgetItem("EURO/USD"))
            self.currency_ratio_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.euro_usd_percantal_ratio))
            
            
            ## Set ttables uneditable.
            self.currency_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.currency_ratio_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.myCurrency_table_buy.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.myCurrency_table_sell.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            
            ## All widgets here.
            self.labelsFont = QtGui.QFont("Trebuchet MS", 11, QtGui.QFont.Bold)
            self.clockFont = QtGui.QFont("Bahnschrift", 11, QtGui.QFont.Normal)
            self.dolar_try = QtWidgets.QLabel()
            self.euro_try = QtWidgets.QLabel()
            self.dolar_euro = QtWidgets.QLabel()
            self.selectLabel = QtWidgets.QLabel("Select a exchange type:")
            self.comboBox = QtWidgets.QComboBox()
            self.inputLabel = QtWidgets.QLabel("Money:")
            self.input = QtWidgets.QLineEdit()
            self.outputLabel = QtWidgets.QLabel("Exchange Result:")
            self.output = QtWidgets.QLabel()
            self.excButton = QtWidgets.QPushButton("Exchange")
            self.tableLabel = QtWidgets.QLabel("STOCK MARKET")
            self.percantalChangeLabel = QtWidgets.QLabel("Percental Change")
            self.accountBalances = QtWidgets.QLabel()
            self.MSGBOX = QtWidgets.QMessageBox()
            self.bringData = QtWidgets.QPushButton("Transaction History")
            self.dataView = QtWidgets.QTextBrowser()
            self.dataView.setText("Click 'Transaction History' button\nfor view your\ntransaction history.")
            self.clearButton = QtWidgets.QPushButton("Clear Transaction History")
            self.currentDateLabel = QtWidgets.QLabel()
            self.currentClockLabel = QtWidgets.QLabel()
            self.graphCurrencyComboBox = QtWidgets.QComboBox()
            self.bringGraphs = QtWidgets.QPushButton("SHOW FOREX GRAPH")
            self.buyTable_Label = QtWidgets.QLabel("Buy table:")
            self.sellTable_Label = QtWidgets.QLabel("Sell table:")
            self.buyRadioButton = QtWidgets.QRadioButton("Buy")
            self.sellRadioButton = QtWidgets.QRadioButton("Sell")
            self.selectLabel2 = QtWidgets.QLabel("Select a currency:")
            self.comboBox2 = QtWidgets.QComboBox()
            self.confirmButton = QtWidgets.QPushButton("Confirm")
            self.balance = QtWidgets.QLabel("")
            self.inputMoney = QtWidgets.QLineEdit()
            
            ## Label set style sheet.
            self.selectLabel.setStyleSheet("QLabel {color: #FFFFFF}")
            self.inputLabel.setStyleSheet("QLabel {color: #FFFFFF}")
            self.outputLabel.setStyleSheet("QLabel {color: #FFFFFF}")
            self.tableLabel.setStyleSheet("QLabel {color: #FF4500}")
            self.percantalChangeLabel.setStyleSheet("QLabel {color: #FF4500}")
            self.outputLabel.setStyleSheet("QLabel {color: #FFFFFF}")
            self.clockLabel.setStyleSheet("QLabel {color: #FFFFFF}")
            self.currentDateLabel.setStyleSheet("QLabel {color: #FFFFFF}")
            self.selectLabel2.setStyleSheet("QLabel {color: 'white';}")
            self.sellTable_Label.setStyleSheet("QLabel {color: 'white';}")
            self.buyTable_Label.setStyleSheet("QLabel {color: 'white';}")    
            self.accountBalances.setStyleSheet("QLabel {color: 'white';}")
            self.output.setStyleSheet("QLabel{color: #66F911;}")
                
            ## Buttons set style sheet.
            self.sellRadioButton.setStyleSheet("QRadioButton {color: #FF5100;}")
            self.buyRadioButton.setStyleSheet("QRadioButton {color: #4FD4FF;}")
            self.excButton.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")
            self.excButton.setFont(self.labelsFont)
            self.confirmButton.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")
            self.bringData.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")    
            self.clearButton.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")
            self.dataView.setStyleSheet("QTextBrowser {background: #969491; color: #000000;}")    
            self.bringGraphs.setStyleSheet("QPushButton {background: #434343; color: white;}")
                
            ## Tables set style sheet.
            self.currency_table.setStyleSheet("QTableWidget {background: #434343; color: #FFA200;}")
            self.currency_table.verticalHeader().setVisible(False)  ## for hide the row-column counter.
            self.currency_table.horizontalHeader().setVisible(False) ## for hide the row-column counter.
            
            self.currency_ratio_table.setStyleSheet("QTableWidget {background: #434343; color: #FFA200;}")
            self.currency_ratio_table.verticalHeader().setVisible(False)
            self.currency_ratio_table.horizontalHeader().setVisible(False)
            
            self.myCurrency_table_buy.setStyleSheet("QTableWidget {background: #434343; color: #FFA200;}")
            self.myCurrency_table_buy.verticalHeader().setVisible(False)
            self.myCurrency_table_buy.horizontalHeader().setVisible(False)
            
            self.myCurrency_table_sell.setStyleSheet("QTableWidget {background: #434343; color: #FFA200;}")
            self.myCurrency_table_sell.verticalHeader().setVisible(False)
            self.myCurrency_table_sell.horizontalHeader().setVisible(False)
            
            ## Combo boxes settings.
            self.comboBox.addItem("Exchange")
            self.comboBox.addItems(["Dolar/TRY","TRY/Dolar","Euro/TRY","TRY/Euro", "Dolar/Euro","Euro/Dolar"])
            self.comboBox2.addItem("Select a currency:")
            self.comboBox2.addItems(["USD","EURO"])
            self.graphCurrencyComboBox.addItem("Select a exchange graph:")
            self.graphCurrencyComboBox.addItems(["USD/TRY","EURO/TRY","EURO/USD"])
            
            ## Combo boxes style adjustments.
            self.graphComboBoxFont = QtGui.QFont("Trebuchet MS", 9, QtGui.QFont.Bold)
            self.graphCurrencyComboBox.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")
            self.graphCurrencyComboBox.setFont(self.graphComboBoxFont)
            self.comboBox.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")
            self.comboBox.setFont(self.graphComboBoxFont)
            self.comboBox2.setStyleSheet("QPushButton {background: #434343; color: #FFA200;}")
            self.comboBox2.setFont(self.graphComboBoxFont)
            
            ## All fonts.
            self.tableFont = QtGui.QFont("Trebuchet MS", 11, QtGui.QFont.Bold)
            self.radioButtonFont = QtGui.QFont("Trebuchet MS", 11, QtGui.QFont.Bold)
            self.textViewFont = QtGui.QFont("Bahnschrift", 11, QtGui.QFont.Light)
            
            self.output.setFont(self.labelsFont)
            self.selectLabel.setFont(self.labelsFont)
            self.inputLabel.setFont(self.labelsFont)
            self.outputLabel.setFont(self.labelsFont)
            self.tableLabel.setFont(self.labelsFont)
            self.clockLabel.setFont(self.clockFont)
            self.currentDateLabel.setFont(self.clockFont)
            self.percantalChangeLabel.setFont(self.labelsFont)
            self.currency_table.setFont(self.tableFont)
            self.currency_ratio_table.setFont(self.tableFont)
            self.myCurrency_table_buy.setFont(self.tableFont)
            self.myCurrency_table_sell.setFont(self.tableFont)
            self.sellRadioButton.setFont(self.radioButtonFont)
            self.buyRadioButton.setFont(self.radioButtonFont)
            self.selectLabel2.setFont(self.labelsFont)
            self.sellTable_Label.setFont(self.labelsFont)
            self.buyTable_Label.setFont(self.labelsFont)
            self.confirmButton.setFont(self.labelsFont)
            self.accountBalances.setFont(self.labelsFont)
            self.bringData.setFont(self.labelsFont)
            self.clearButton.setFont(self.labelsFont)
            self.dataView.setFont(self.textViewFont)
            self.bringGraphs.setFont(self.labelsFont)
            

            ## Alignment settings.
            self.output.setAlignment(QtCore.Qt.AlignCenter)
            self.outputLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.tableLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.percantalChangeLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.clockLabel.setAlignment(QtCore.Qt.AlignLeft)
            self.accountBalances.setAlignment(QtCore.Qt.AlignRight)
            self.currentDateLabel.setAlignment(QtCore.Qt.AlignRight)

            
            ## Timing settings.
            self.currentDateTime = datetime.datetime.now()
            self.clock = self.currentDateTime.strftime("%H:%M")
            self.today = self.currentDateTime.strftime("%d/%m/%Y")
            self.clockLabel.setText("{}".format(self.clock))
            self.currentDateLabel.setText("{}".format(self.today))
            
            
            ## Forex Graph view.
            self.forexGraph = QtWebEngineWidgets.QWebEngineView()
            self.forexGraph.load(QtCore.QUrl('https://www.tradingview.com/chart/?symbol=FX%3AUSDTRY'))
            
            
            ## Layout part.
            v_box = QtWidgets.QVBoxLayout()
            v_box2 = QtWidgets.QVBoxLayout()
            v_box3 = QtWidgets.QVBoxLayout()

            ## V_BOX (LEFT)
            v_box.addWidget(self.clockLabel)
            v_box.addWidget(self.tableLabel)
            v_box.addWidget(self.currency_table)
            v_box.addWidget(self.percantalChangeLabel)
            v_box.addWidget(self.currency_ratio_table)
            v_box.addWidget(self.selectLabel)
            v_box.addWidget(self.comboBox)
            v_box.addWidget(self.inputLabel)
            v_box.addWidget(self.input)
            v_box.addWidget(self.outputLabel)
            v_box.addWidget(self.output)
            v_box.addWidget(self.excButton)
            v_box.addWidget(self.dataView)
            
            ## V_BOX3 (MIDDLE)
            v_box3.addWidget(self.graphCurrencyComboBox)
            v_box3.addWidget(self.forexGraph)
            v_box3.addWidget(self.bringGraphs)
            
            ## V_BOX2 (RIGHT)
            v_box2.addWidget(self.currentDateLabel)
            v_box2.addWidget(self.buyTable_Label)
            v_box2.addWidget(self.myCurrency_table_buy)
            v_box2.addWidget(self.sellTable_Label)
            v_box2.addWidget(self.myCurrency_table_sell)
            v_box2.addWidget(self.accountBalances)
            v_box2.addWidget(self.buyRadioButton)
            v_box2.addWidget(self.sellRadioButton)
            v_box2.addWidget(self.selectLabel2)
            v_box2.addWidget(self.comboBox2)
            v_box2.addWidget(self.inputMoney)
            v_box2.addWidget(self.confirmButton)
            v_box2.addWidget(self.bringData)
            v_box2.addWidget(self.clearButton)
            
            h_box = QtWidgets.QHBoxLayout()
    
            h_box.addStretch()
            h_box.addLayout(v_box)
            h_box.addLayout(v_box3)
            h_box.addLayout(v_box2)
            h_box.addStretch()

            self.set_myCurrencyRate_text() ## set currency values with fee. 
            self.showBalances() ## show balance.
            self.colorRatios()
            
            self.setLayout(h_box)
            self.show()
    
            ## FUNCTION CONNECTIONS
            self.excButton.clicked.connect(self.exchange)
            self.confirmButton.clicked.connect(lambda: self.trade(self.buyRadioButton.isChecked(), self.sellRadioButton.isChecked()))
            self.bringData.clicked.connect(self.bringAllData)
            self.clearButton.clicked.connect(self.clear_text_view)
            self.bringGraphs.clicked.connect(self.bringForexGraph)
            
            ## CONTROLLING THE INTERNET CONNECTION. IF INTERNET CONNECTION LOST OR NOT FIND IT WILL GIVE A ERROR MESSAGE.
        except ConnectionError as e:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("ERROR! No connection. Check your internet connection please.")
            self.msgBox.setWindowTitle("Critical")
            self.msgBox.exec_()
    
    ## Refreshing all of the values.
    def refreshMarket(self):
        
        try: 
            page = requests.get('https://www.bloomberght.com')
            soup = BeautifulSoup(page.content, 'html.parser')
            currency = soup.find(class_='col-md-10 col-sm-12 col-xs-12 marketsWrap')
            currency_dolar = currency.find(id = "dolar")
            currency_euro = currency.find(id = "euro")
            currency_euro_usd = currency.find(id="eur-usd")
            currency_value_eurusd = currency_euro_usd.select(".LastPrice")
            currency_value_dolar = currency_dolar.select(".LastPrice")
            currency_value_euro = currency_euro.select(".LastPrice")
            getting_closer = currency.find_all(class_="marketsCol")
            
            try:
                self.usd_try_percantal_ratio = getting_closer[1].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.usd_try_percantal_ratio = getting_closer[1].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.usd_try_percantal_ratio = "0.00"

            try:
                self.euro_try_percantal_ratio = getting_closer[2].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_try_percantal_ratio = getting_closer[2].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_try_percantal_ratio = "0.00"
    
            try:
                self.euro_usd_percantal_ratio = getting_closer[3].find(class_="downRed PercentChange").get_text()
            except AttributeError:
                try:
                    self.euro_usd_percantal_ratio = getting_closer[3].find(class_="upGreen PercentChange").get_text()
                except AttributeError:
                    self.euro_usd_percantal_ratio = "0.00"
                
            self.temp_value1 = currency_value_dolar[0].get_text()
            self.temp_value2 = currency_value_euro[0].get_text()
            self.temp_value3 = currency_value_eurusd[0].get_text()
            
            self.value1 = self.temp_value1.replace(',','.')
            self.value2 = self.temp_value2.replace(',','.')
            self.value3 = self.temp_value3.replace(',','.')
            
            self.currency_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.value1))
            
            self.currency_table.setItem(1,0, QtWidgets.QTableWidgetItem("EUR/TRY"))
            self.currency_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.value2))
            
            self.currency_table.setItem(2,0, QtWidgets.QTableWidgetItem("EUR/USD"))
            self.currency_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.value3))
            
            self.currency_ratio_table.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
            self.currency_ratio_table.setItem(0,1, QtWidgets.QTableWidgetItem(self.usd_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(1,0, QtWidgets.QTableWidgetItem("EURO/TRY"))
            self.currency_ratio_table.setItem(1,1, QtWidgets.QTableWidgetItem(self.euro_try_percantal_ratio))
            
            self.currency_ratio_table.setItem(2,0, QtWidgets.QTableWidgetItem("EURO/USD"))
            self.currency_ratio_table.setItem(2,1, QtWidgets.QTableWidgetItem(self.euro_usd_percantal_ratio))
            
            
            self.set_myCurrencyRate_text() ## refresh currency values w/ fee.
            self.showBalances() ## refresh balance, too.

            ## AGAIN, SAME INTERNET CONNECTION CONTROLLING.
        except ConnectionError:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            self.msgBox.setText("ERROR! No connection. Check your internet connection please.")
            self.msgBox.setWindowTitle("Critical")
            self.msgBox.exec_()
    
    ## EXCHANGE PROCESS.
    def exchange(self):
        
        try:
            comboText = self.comboBox.currentText() ## TAKEN COMBOBOX SELECTION AND DOING CALCULATIONS ACCORDING TO SELECTION.
            
            if comboText == "Dolar/TRY":
    
                result_dolar_try = float(self.input.text())  * float(self.value1)
                result_dolar_try = "{:.4f}".format(result_dolar_try)
                self.output.setText(str(result_dolar_try) + " TRY")
            
            elif comboText == "TRY/Dolar":
    
                result_try_dolar = float(self.input.text()) / float(self.value1)
                result_try_dolar = "{:.4f}".format(result_try_dolar)
                self.output.setText(str(result_try_dolar) + " $")
    
            elif comboText == "Euro/TRY":
    
                result_try_euro = float(self.input.text()) * float(self.value2)
                result_try_euro = "{:.4f}".format(result_try_euro)
                self.output.setText(str(result_try_euro) + " TRY")
    
            elif comboText == "TRY/Euro":
    
                result_euro_try = float(self.input.text()) / float(self.value2)
                result_euro_try = "{:.4f}".format(result_euro_try)
                self.output.setText(str(result_euro_try) + " €")
    
            elif comboText == "Dolar/Euro":
    
                result_dolar_euro = float(self.input.text()) / float(self.value3)
                result_dolar_euro = "{:.4f}".format(result_dolar_euro)
                self.output.setText(str(result_dolar_euro) + " €") 
    
            elif comboText == "Euro/Dolar":
    
                result_euro_dolar = float(self.input.text()) * float(self.value3)
                result_euro_dolar= "{:.4f}".format(result_euro_dolar)
                self.output.setText(str(result_euro_dolar) + " $")
                
            else:
                self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                self.msgBox.setText("Please select an exchange first.")
                self.msgBox.setWindowTitle("Warning")
                self.msgBox.exec_()
        
        ## AN ERROR MESSAGE.
        except ValueError:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            self.msgBox.setText("Error! No input taken.")
            self.msgBox.setWindowTitle("An error occured")
            self.msgBox.exec_()


    def showTime(self):
        
        ## AFTER 30 SECONDS THIS FUNCTION WILL RUN AND IT WILL RUN THE REFRESH MARKET TOO.
        self.refreshMarket()
        self.colorRatios() ## OF COURSE THE COLOR ADJUSTMENTS WILL RUN TOO.
        self.currentDateTime = datetime.datetime.now()
        self.clock = self.currentDateTime.strftime("%H:%M")
        self.today = self.currentDateTime.strftime("%d/%m/%Y")
        self.clockLabel.setText("{}".format(self.clock))
        self.currentDateLabel.setText("{}".format(self.today))
        
        
    def colorRatios(self):
        
        ## TEMPORARY VARIABLES. WE REPLACE "," TO "." BECAUSE
        ## WE HAVE TO CONTROL THE VALUE. WITH THAT WAY WE CAN GIVE RED COLOR FOR NEGATIVE PERCENTAL CHANGE VALUES
        ## AND WE CAN GIVE GREEN COLOR FOR POSITIVE PERCENTAL CHANGE VALUES.
        new_usd_try_ratio_temp = self.usd_try_percantal_ratio.replace("% ","")
        new_usd_try_ratio = new_usd_try_ratio_temp.replace(",",".")
        
        new_euro_try_ratio_temp = self.euro_try_percantal_ratio.replace("% ","")
        new_euro_try_ratio = new_euro_try_ratio_temp.replace(",",".")

        new_euro_usd_ratio_temp = self.euro_usd_percantal_ratio.replace("% ","")
        new_euro_usd_ratio = new_euro_usd_ratio_temp.replace(",",".")

        ## CONTROLLING BEGINS.
        if float(new_usd_try_ratio) < 0:
            self.currency_ratio_table.item(0,1).setBackground(QtGui.QColor(100,0,0)) ## GREEN

        if float(new_euro_try_ratio) < 0:
            self.currency_ratio_table.item(1,1).setBackground(QtGui.QColor(100,0,0))

        if float(new_euro_usd_ratio) < 0:
            self.currency_ratio_table.item(2,1).setBackground(QtGui.QColor(100,0,0))
            
        if float(new_usd_try_ratio) > 0:
            self.currency_ratio_table.item(0,1).setBackground(QtGui.QColor(0,100,0)) ## RED

        if float(new_euro_try_ratio) > 0:
            self.currency_ratio_table.item(1,1).setBackground(QtGui.QColor(0,100,0))

        if float(new_euro_usd_ratio) > 0:
            self.currency_ratio_table.item(2,1).setBackground(QtGui.QColor(0,100,0))
            
        ## WHEN PERCENTAL CHANGE VALUE BE %0.00, THERE IS NO COLOR ASSIGNED.
            
        
    def trade(self, controlling_buy, controlling_sell):
        
        ## NOW, THIS PART IS IMPORTANT. BECAUSE IN THIS PART, THERE IS A INSERT PROCESS AND A CALUCLATION PROCESS.
        
        cbText = self.comboBox2.currentText()  ## FIRST WE MAKE SURE WHICH CURRENCY THAT WILL USE THE USER.
        
        self.cursor.execute("SELECT usd FROM account")  ## TAKING DATA. BECAUSE WE HAVE TO HOLD NEWEST DATA IN DATABASE.
        self.usd_balance = self.cursor.fetchone()[0]    ## IN EVERY CALCULATION/OPERATION/TRADE WE WILL USE THESE DATA.
        
        self.cursor.execute("SELECT eur FROM account")
        self.eur_balance = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT try FROM account")
        self.try_balance = self.cursor.fetchone()[0]


        self.cursor.execute("SELECT usd FROM myAccount")        ## THESE DATA FOR THE COMPANY/BANK IT IS THEIR INCOME, OR MINE :P
        self.myAccount_usd_balance = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT eur FROM myAccount")
        self.myAccount_eur_balance = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT try FROM myAccount")
        self.myAccount_try_balance = self.cursor.fetchone()[0]
        
        ## First of all, there is a try-except block for controlling AttributeError. We take this error when user don't write any input/number.
        ## After that, we're controlling which transaction selected. Is the operation buying or selling? 2 parameters that we took before will be useful in this part.
        ## When the operation be defined, we can control which currency will be use. After that, we have to control user's balance.
        ## Then, If everything is ok, we can make the operation what user want.
        ## Lastly, we run the showBalance()  function for refreshed the balance after operation and we run the transactionInsert() function.
        ## This function will be use for insert the transaction information in the our database. We take every single information and insert it.
        ## Of course all of the changes, will update in database. You can just look at first block, remain blocks are running same as same first block.
        ## There are just a few calculation differences between buy and sell of course.
        
        
        #  try block.
        try:
            if controlling_buy == True:             ## buy or sell? It returns boolean.
                if cbText == "USD":                 ## which currency?
                    self.control_try_balance()      ## conrol balance.
                    if self.isEverythingOK == True: ## balance is ok or not ok?
                        ## operation begins.
                        fee_usd = (float(self.value1) / 100) * 1.45
                        newUsdRate = fee_usd + float(self.value1)
                        lostTRY = float(self.inputMoney.text()) * newUsdRate
                        self.account_new_try_balance = self.try_balance - lostTRY                  
                        self.account_new_usd_balance = self.usd_balance + float(float(self.inputMoney.text()))
                        self.myIncome = ((lostTRY - (float(self.value1) * float(self.inputMoney.text()))) / float(self.value1)) + self.myAccount_usd_balance
                        self.fee = ((lostTRY - (float(self.value1) * float(self.inputMoney.text()))) / float(self.value1))
                        
                        ## updating data.
                        self.cursor.execute("UPDATE myAccount SET usd  = ? WHERE usd = ?",(self.myIncome, self.myAccount_usd_balance))
                        self.cursor.execute("UPDATE account SET usd = ? WHERE usd = ?",(self.account_new_usd_balance, self.usd_balance))
                        self.cursor.execute("UPDATE account SET try = ? WHERE try = ?",(self.account_new_try_balance, self.try_balance))
                        self.conn.commit()
                        
                        self.showBalances() ## update balance label.
                        self.whichCurrency = "$"   ## will be use for transaction information inserting.
                        self.transtactionInsert(lostTRY, float(self.inputMoney.text()), self.fee, self.whichCurrency, controlling_buy, controlling_sell,newUsdRate)   # letz' go     
                        
                if cbText == "EURO":
                    self.control_try_balance()
                    if self.isEverythingOK == True:
                        
                        fee_euro = (float(self.value2) / 100) * 1.22
                        newEurRate = fee_euro + float(self.value2)
                        lostTRY = float(self.inputMoney.text()) * newEurRate
                        self.account_new_try_balance = self.try_balance - lostTRY                  
                        self.account_new_euro_balance = self.eur_balance + float(float(self.inputMoney.text()))
                        self.myIncome = ((lostTRY - (float(self.value2) * float(self.inputMoney.text()))) / float(self.value2)) + self.myAccount_eur_balance
                        self.fee = ((lostTRY - (float(self.value2) * float(self.inputMoney.text()))) / float(self.value2))
                        
                        self.cursor.execute("UPDATE myAccount SET eur = ? WHERE eur = ?",(self.myIncome, self.myAccount_eur_balance))
                        self.cursor.execute("UPDATE account SET eur = ? WHERE eur = ?",(self.account_new_euro_balance, self.eur_balance))
                        self.cursor.execute("UPDATE account SET try = ? WHERE try = ?",(self.account_new_try_balance, self.try_balance))
                        self.conn.commit()
                        
                        self.showBalances()
                        self.whichCurrency = "€"
                        self.transtactionInsert(lostTRY, float(self.inputMoney.text()), self.fee, self.whichCurrency,controlling_buy, controlling_sell, newEurRate)  
                        
            if controlling_sell == True:
                if cbText == "USD":
                    self.control_usd_balance()
                    if self.isEverythingOK2 == True:
                        
                        fee_usd = (float(self.value1) / 100) * 0.69
                        newUsdRate = float(self.value1) - fee_usd
                        self.account_new_usd_balance = self.usd_balance - float(self.inputMoney.text())
                        boughtTRY = float(self.inputMoney.text()) * newUsdRate
                        self.account_new_try_balance = boughtTRY + self.try_balance
                        self.myIncome = (((float(self.value1) * float(self.inputMoney.text()))- boughtTRY) / float(self.value1)) + self.myAccount_usd_balance
                        self.fee = (((float(self.value1) * float(self.inputMoney.text()))- boughtTRY) / float(self.value1))
                        
                        self.cursor.execute("UPDATE myAccount SET usd = ? WHERE usd = ?",(self.myIncome, self.myAccount_usd_balance))
                        self.cursor.execute("UPDATE account SET usd = ? WHERE usd = ?",(self.account_new_usd_balance, self.usd_balance))
                        self.cursor.execute("UPDATE account SET try = ? WHERE try = ?",(self.account_new_try_balance, self.try_balance))
                        self.conn.commit()
                        
                        self.showBalances()
                        self.whichCurrency = "$"
                        self.transtactionInsert(float(self.inputMoney.text()), boughtTRY, self.fee, self.whichCurrency,controlling_buy, controlling_sell,newUsdRate)  
    
                if cbText == "EURO":
                    self.control_eur_balance()
                    if self.isEverythingOK3 == True:
                        
                        fee_euro = (float(self.value2) / 100) * 0.61
                        newEurRate = float(self.value2) - fee_euro
                        self.account_new_eur_balance = self.eur_balance - float(self.inputMoney.text())
                        boughtTRY = float(self.inputMoney.text()) * newEurRate
                        self.account_new_try_balance = boughtTRY + self.try_balance
                        self.myIncome = (((float(self.value2) * float(self.inputMoney.text()))- boughtTRY) / float(self.value2)) + self.myAccount_eur_balance
                        self.fee = (((float(self.value2) * float(self.inputMoney.text()))- boughtTRY) / float(self.value2))
                        
                        self.cursor.execute("UPDATE myAccount SET eur = ? WHERE eur = ?",(self.myIncome, self.myAccount_eur_balance))
                        self.cursor.execute("UPDATE account SET try = ? WHERE try = ?",(self.account_new_try_balance, self.try_balance))
                        self.cursor.execute("UPDATE account SET eur = ? WHERE eur = ?",(self.account_new_eur_balance, self.eur_balance))
                        self.conn.commit()
                        
                        self.showBalances()
                        self.whichCurrency = "$"
                        self.transtactionInsert(float(self.inputMoney.text()), boughtTRY, self.fee, self.whichCurrency,controlling_buy, controlling_sell,newEurRate)
                        
            if controlling_buy == False and controlling_sell == False:
                
                 self.MSGBOX.setIcon(QtWidgets.QMessageBox.Warning)
                 self.MSGBOX.setText("Please choose a transaction.")
                 self.MSGBOX.setWindowTitle("An error occured.")
                 self.MSGBOX.exec_()
        except AttributeError:
             self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
             self.msgBox.setText("Check your inputs please.")
             self.msgBox.setWindowTitle("Information")
             self.msgBox.exec_()
    
    ## controlling balance
    def control_try_balance(self):
         
        try:
            self.isItEnough = self.try_balance - float(self.inputMoney.text())
             
            if self.isItEnough > 0:
                 self.isEverythingOK = True
            else:
                 self.isEverythingOK = False
                 self.MSGBOX.setIcon(QtWidgets.QMessageBox.Critical)
                 self.MSGBOX.setText("You do not have enough money.")
                 self.MSGBOX.setWindowTitle("An error occured.")
                 self.MSGBOX.exec_()
             
        except ValueError:
             self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
             self.msgBox.setText("Error! No input taken.")
             self.msgBox.setWindowTitle("Critical")
             self.msgBox.exec_()
             
    ## controlling balance    
    def control_usd_balance(self):
        try:
            self.isItEnough2 = self.usd_balance - float(self.inputMoney.text())
            
            if self.isItEnough2 > 0:
                self.isEverythingOK2 = True
            else:
                self.isEverythingOK2 = False
                self.MSGBOX.setIcon(QtWidgets.QMessageBox.Critical)
                self.MSGBOX.setText("You do not have enough money.")
                self.MSGBOX.setWindowTitle("An error occured.")
                self.MSGBOX.exec_()
                
        except ValueError:
             self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
             self.msgBox.setText("Error! No input taken.")
             self.msgBox.setWindowTitle("Critical")
             self.msgBox.exec_()
             
    ## controlling balance           
    def control_eur_balance(self):
        
        try:
            self.isItEnough3 = self.eur_balance - float(self.inputMoney.text())
        except ValueError:
            self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            self.msgBox.setText("Error! No input taken.")
            self.msgBox.setWindowTitle("Critical")
            self.msgBox.exec_()
        
        if self.isItEnough3 > 0:
            self.isEverythingOK3 = True
        else:
            self.isEverythingOK3 = False
            self.MSGBOX.setIcon(QtWidgets.QMessageBox.Critical)
            self.MSGBOX.setText("You do not have enough money.")
            self.MSGBOX.setWindowTitle("An error occured.")
            self.MSGBOX.exec_()
    
    ## The bank or company currency values.
    def set_myCurrencyRate_text(self):
        myCurrency_Dolar_buy = (((float(self.value1) / 100) * 1.45) + float(self.value1))
        myCurrency_Euro_buy = (((float(self.value2) / 100) * 1.22) + float(self.value2))
        
        myCurrency_Dolar_sell = (float(self.value1) - ((float(self.value1) / 100) * 0.69))
        myCurrency_Euro_sell = (float(self.value2) - ((float(self.value2) / 100) * 0.61))
        
        ## Data inserting in buy/sell tables.
        self.myCurrency_table_buy.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
        self.myCurrency_table_buy.setItem(0,1, QtWidgets.QTableWidgetItem("{:.3f}".format(myCurrency_Dolar_buy)))
        
        self.myCurrency_table_buy.setItem(1,0, QtWidgets.QTableWidgetItem("EUR"))
        self.myCurrency_table_buy.setItem(1,1, QtWidgets.QTableWidgetItem("{:.3f}".format(myCurrency_Euro_buy)))
        
        self.myCurrency_table_sell.setItem(0,0, QtWidgets.QTableWidgetItem("USD/TRY"))
        self.myCurrency_table_sell.setItem(0,1, QtWidgets.QTableWidgetItem("{:.3f}".format(myCurrency_Dolar_sell)))
        
        self.myCurrency_table_sell.setItem(1,0, QtWidgets.QTableWidgetItem("EUR/TRY"))
        self.myCurrency_table_sell.setItem(1,1, QtWidgets.QTableWidgetItem("{:.3f}".format(myCurrency_Euro_sell)))
        
    
    ## Showing user balance.
    def showBalances(self):
        
        self.cursor.execute("SELECT usd FROM account")
        self.usd_balance = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT eur FROM account")
        self.eur_balance = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT try FROM account")
        self.try_balance = self.cursor.fetchone()[0]
        
        self.accountBalances.setText("Your balance:\n${:.2f}\n€{:.2f}\n₺{:.2f}".format(self.usd_balance, self.eur_balance, self.try_balance))
        
    
    ## We give 6 paramters. Every operation is in restricted.    
    def transtactionInsert(self, lostMoney, boughtMoney, fee, whichCurrency, control_buy, control_sell,currencyVal_):

        
        now2 = datetime.datetime.now()  ## For write operation date time.
        
        if control_buy == True:  ## buy
            if whichCurrency == "$":  ## which curreny. after that insert process begins.
                self.cursor.execute("INSERT INTO transactions VALUES(?,?,?,?,?)",("{}/{}/{} ~ {}:{}".format(now2.day,now2.month,now2.year, now2.hour, now2.minute), "{:.2f}TRY".format(lostMoney), "{:.2f}$".format(boughtMoney), "{:.2f}$".format(fee),"{:.2f}$".format(currencyVal_)))
                self.conn.commit()
            if whichCurrency == "€":
                self.cursor.execute("INSERT INTO transactions VALUES(?,?,?,?,?)",("{}/{}/{} ~ {}:{}".format(now2.day,now2.month,now2.year, now2.hour, now2.minute), "{:.2f}TRY".format(lostMoney), "{:.2f}€".format(boughtMoney), "{:.2f}€".format(fee), "{:.2f}€".format(currencyVal_)))
                self.conn.commit()
        
        if control_sell == True:  ## sell
            if whichCurrency == "$":
                self.cursor.execute("INSERT INTO transactions VALUES(?,?,?,?,?)",("{}/{}/{} ~ {}:{}".format(now2.day,now2.month,now2.year, now2.hour, now2.minute), "{:.2f}$".format(lostMoney), "{:.2f}TRY".format(boughtMoney), "{:.2f}$".format(fee), "{:.2f}$".format(currencyVal_)))
                self.conn.commit()
            if whichCurrency == "€":
                self.cursor.execute("INSERT INTO transactions VALUES(?,?,?,?,?)",("{}/{}/{} ~ {}:{}".format(now2.day,now2.month,now2.year, now2.hour, now2.minute), "{:.2f}€".format(lostMoney), "{:.2f}TRY".format(boughtMoney), "{:.2f}€".format(fee), "{:.2f}€".format(currencyVal_)))
                self.conn.commit()
    
    ## Creating a text. We write all data into this file. After that, we take these data and write it into the QTextView widget.
    def bringAllData(self):
        
        ## creating file
        data_information = open("transaction_brief.txt", "w+")
        
        ## Taking data from database.
        self.cursor.execute("SELECT datetime FROM transactions")
        datetimes = self.cursor.fetchall()

        self.cursor.execute("SELECT soldMoney FROM transactions")
        soldMoney = self.cursor.fetchall()

        self.cursor.execute("SELECT boughtMoney FROM transactions")
        boughtMoney = self.cursor.fetchall()

        self.cursor.execute("SELECT fee FROM transactions")
        fee = self.cursor.fetchall()
        
        self.cursor.execute("SELECT currencyVal FROM transactions")
        currencyVal = self.cursor.fetchall()

        myListLength = len(list(datetimes))  # this length value, gives us how many times for loop will run. we will write all transaction information with that way.
        
        for i in range(0,myListLength):
            data_information.write("Transaction [{}]\nDate Time: {}\nSold Money: {}\nBought Money: {}\nFee: {}\nCurrency Value:{}\n\n".format(i,list(datetimes[i]), list(soldMoney[i]), list(boughtMoney[i]), list(fee[i]), list(currencyVal[i])))
        
        ## writing done.
        
        data_information.close()  ## file closed.
        self.set_data_in_textview() ## letz go
  
    def set_data_in_textview(self):
        
        ## open the file as read mode which includes all data inside it.
        data_information = open("transaction_brief.txt", "r")
        transaction_information = data_information.read()  ## read file. content defined.
        
        self.dataView.setText(transaction_information)  ## content wrote into the QTabView widget.
        
        if len(transaction_information) <= 0:       ## If the file is empty.
            self.dataView.setText("Not found any transaction.")
            
    def clear_text_view(self): #clear QTabView content.
        self.dataView.clear()
    
    ## Which exchange graph we will show the user defined in this function.
    def bringForexGraph(self):
        
        comboText2 = self.graphCurrencyComboBox.currentText()
        if comboText2 == "USD/TRY":
            self.forexGraph.load(QtCore.QUrl('https://www.tradingview.com/chart/?symbol=FX%3AUSDTRY'))
        elif comboText2 == "EURO/TRY":
            self.forexGraph.load(QtCore.QUrl('https://www.tradingview.com/chart/?symbol=FX_IDC%3ATRYEUR'))
        elif comboText2 == "EURO/USD":
            self.forexGraph.load(QtCore.QUrl('https://www.tradingview.com/chart/?symbol=FX_IDC%3AEURUSD'))
            
                                        
            
app = QtWidgets.QApplication(sys.argv)
window = Window()
window.move(200, 120)
app.setStyle("Fusion")
window.setFixedSize(1355, 590)
window.setStyleSheet("Window {background : #4E4E4E;}")
sys.exit(app.exec_())





