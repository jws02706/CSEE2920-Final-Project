import hashlib as hasher
import time
import csv
import random
import RPi.GPIO as GPIO
import socket
!/usr/bin/python
import sys
import Adafruit_DHT

class Block:
	#attributes
	index = 0
	prevHash = None
	timeStamp = None
	zipcode = 0
	isSeller = False
	tempData = 0
	avgTempData = 0
	lightData = 0
	nonce = 0
	ldrPin = 7 #defining the ldr pin in the program
	didTransactionOccured = False
	
	##
	#   Acts as the constructor of the block functions
	#
	#   @param self              A block object allowing to access its attributes
	#   @param index             Index of where the block is located
	#   @param timestamp         The time when the block was created
	#   @param zipcode           The location where the block belongs to
	#   @param isSeller          A boolean to describe whether the block is a solar producer or a 
	#   @param tempData          The temperature that the device detected
	#   @param lightData         The light data that the device detected
	#   @param balance           A balance of the block
	#   @param prevHash          The hash that block will connect to in the previous block in blockchain
	##
	def __init__(self, index, timestamp, zipcode, isSeller, tempData, lightData, balance, prevHash):
		self.index = index
		self.prevHash = ''
		self.timestamp = timestamp
		self.zipcode = zipcode
		self.isSeller = isSeller
		self.tempData = 0
		self.lightData = 0
		self.nonce = 0
		
		#setting the data if the block belongs to the solar producer
		if self.isSeller == True:
			self.tempData = tempData
			self.lightData = lightData
		
		self.balance = balance
		self.hash = self.calculateHash
		
	##
	#   Haves the block to declare if it is making a transaction
	#
	#   @param isTransacting       A boolean to declare that a device is transacting
	##
	def declareTransaction(self, isTransacting):
		if self.isSeller == False:
			if isTransaction == True:
				didTransactionOccured = True:
	
	##
	#  Calculate the hash of a block
	#
	#  @param self             The hlock to access the attributes within this class
	##
	def calculateHash(self):
		sha = hasher.sha256()
		sha.update(str(self.index)+ 
				   str(self.prevHash) + 
				   str(self.timestamp) + 
				   str(self.zipcode) + 
				   str(self.nonce))
		return sha.hexdigest()
	
	## 
	#  Mines the block for its hash
	#
	#  @param self             The block to access the attributes within this class
	#  @param level            The level of difficulty for encryption for a block to hash
	##
	def mineBlock(self, level):
		#obtaining original hashing for comparison
		hashStr = ""
		for i in range(0, level):
			hashStr += self.hash[i]
		
		#obtaining a list of number of zeros for comaprison
		comparisonStr = ""
		for j in range(j, level+1): ##CHECK THIS--
			comparisonStr += "0"
		
		#comparing the two string to continue to mine
		while hashStr != comparisonStr:
			self.nonce += 1
			self.hash = self.calculateHash()
		
		print("BLOCK MINED: " , self.hash)
		
	## 
	#  Adds a temperature to a block
	#
	#  @param self             The block to access the attributes within this class
	#  @param data             The temperature data to manually input in
	##
	def addTemp(self, data):
		self.tempData = data
	
	## 
	#  Converts a binary to a decimal
	#
	#  @param string_num       The string to be converted
	#
	#  @return                 The decimal number
	##
	def bin2dec(string_num):
		return str(int(string_num, 2))
	
	## 
	#  Gets a temperature to a block
	#
	#  @param pin              The pin where the temperature sensor will be connected in Pi
	#  
	#  @return                 The temperature in Celcius
	##
	
	#NOTE: PIN 4 for connection
	#source: circuit basic
	def getTemp(pin):
		#printing only once for demostration
		humidity, temperature = Adafruit_DHT.read_retry(11, pin)
		print("Temp: %d C" % temperature)
		return temperature
	
	## 
	#  Gets a temperature to a block
	#
	#  @param pin              The pin where the temperature sensor will be connected in Pi
	#  
	#  @return                 The temperature in Celcius
	##
	
	#NOTE: PIN 4 for connection
	def getTemp2(pin):
		data = []
		
		#setting up the GPIO pins
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(0.025) #Delay
		GPIO.output(pin, GPIO.LOW)
		time.sleep(0.02)
		GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		#gathering data
		for i in range(0, 500):
			data.append(GPIO.input(pin))
		
		bit_count = 0
		tmp = 0
		count = 0
		temp_bit = ""
		humidity_bit = ""
		crc = ""
		
		try:
			while data[count] == 1:
				tmp = 1
				count += 1
			
			for j in range(0, 32):
				bit_count = 0
				
				while data[count] == 0:
					tmp = 1
					count += 1
				
				if bit_count > 3:
					if j >= 0 and j < 8:
						humidity_bit = humidity_bit + "1"
					if j >= 16 and j < 24:
						temp_bit = temp_bit + "1"
				else:
					if j >= 0 and j < 8:
						humidity_bit = humidity_bit + "0"
					if j >= 16 and j < 24:
						temp_bit = temp_bit + "0"
		except:
			print("ERR RANGE")
			exit(0)
		
		try:
			for k in range(0, 8):
				bit_count = 0
				
				while data[count] == 0:
					tmp = 1
					count = count + 1
				
				while data[count] == 1:
					bit_count = bit_count + 1
					count = count + 1
				
				if bit_count > 3:
					crc = crc + "1"
				else:
					crc = crc + "0"
		except:
			print("ERR RANGE")
			exit(0)
		
		#obtaining a value for temperature to be return
		humidity = bin2dec(humidity_bit)
		temp = bin2dec(temp_bit)
		tempVal = -1 # return value
		
		if int(humidity) + int(temp) - int(bin2dec(crc)) == 0:
			tempVal = int(temp)
		else:
			print("ERR_CRC")
		
		return tempVal
	
	#LDR Functions (Next Three)
	## 
	#  Calculate the time for the sensor to obtain data
	#
	#  @param ldrPin   The pin that the sensor is connected to the Pi
	#  
	#  @return                 The time it takes for a sensor to obtain data
	##
	def rc_time (ldrPin):
		count = 0
	  
		#Output on the pin for 
		GPIO.setup(ldrPin, GPIO.OUT)
		GPIO.output(ldrPin, GPIO.LOW)
		time.sleep(0.1)

		#Change the pin back to input
		GPIO.setup(ldrPin, GPIO.IN)
	  
		#Count until the pin goes high
		while (GPIO.input(ldrPin) == GPIO.LOW):
			count += 1

		return count
		
	## 
	#   Sets up the LDR sensor
	#	@param self             The block to access the attributes within this class
	#
	##
	def setLDR(self):
		GPIO.setmode(GPIO.BOARD)
		
	## 
	#  Return the LDR data
	#
	#  @param self             The block to access the attributes within this class
	#
	#  @return                 The LDR data
	##
	def getLDR(self):
		setLDR();
		
		#Catch when script is interupted, cleanup correctly
		try:
			# Main loop
			while True:
				return rc_time(ldrPin)
		except KeyboardInterrupt:
			pass
		finally:
			GPIO.cleanup()
	
class Blockchain:

	#attributes
	numBlocks = 0
	chain = []
	level = 5
	prevAvgTemp = 0
	message = '';
	
	##
	#   Acts as the constructor of the block functions
	#
	#   @param self              A blockchain object allowing to access its attributes
	##
	def __init__(self):
		self.chain.append(self.createGenesisBlock())
		
	## 
	#  Starts the blockchain
	#
	#  @param self             The blockchain object to access the attributes within this class
	##
	def startChain(self):
		tempBlock = self.createGenesisBlock()
		self.chain.append(tempBlock)
	
	## 
	#  Creates the genesis block for the blockchain
	#
	#  @param self             The blockchain object to access the attributes within this class
	#
	#  @return                 The genesis block
	##
	def createGenesisBlock(self):
		self.numBlocks += 1
		originBlock = Block(self, 0, "01/01/2017", "30609", True, 30, 40, 0)
		#print('Test -- Seeing to enter self function')
		return originBlock
	
	##
	#   Get the latest block from the blockchain
	#
	#   @return                The latest block from the blockchain
	##
	def getLatestBlock(self):
		return self.chain[self.chain.length - 1]
	
	##
	#   Get the number of blocks within the blockchain
	#
	#   @return                The number of blocks in a blockchain
	##
	def countBlocks(self):
		return self.chain.length
	
	#add blocks to be written late
	##
	#   Adds a block to the blockchain
	#
	#   @param self             The blockchain object to access the attributes within this class
	#   @param newBlock         The block to be added onto the blockchain
	##
	def addBlock(self, newBlock):
		if newBlock.zipcode == self.chain[0].zipcode:
			newBlock.prevHash = self.getLatestBlock().hash
			newBlock.mineBlock(self.level)
			self.chain.push(newBlock)
			self.numBlocks += 1
			
			#checking the indices to make sure they are not repeated
			isIndexSame = False
			i = 0
			
			##Rewritten from FOR LOOP --> CHECK THIS IF THERE IS A PROBLEM
			while i < (self.chain.length-1) and isIndexSame == False:
				if newBlock.index == self.chain[i].index:
					isIndexSame = True
				i+=1
			
			if isIndexSame == True:
				print('The index of self new block already exiats!') #ERROR MESSAGE
				print('The index of self new block will be ', self.numBlocks)
				newBlock.index = self.numBlocks;
			
			#print out a successful message
			print('These blocks match in the chain!')
			
		else:
			print('Cannot add self block due to hashing not match!')
	
	##
	#   Checks to see if the blockchain is valid
	#
	#   @param self             The blockchain object to access the attributes within this class
	#   
	#   @return                 A boolean to tell whether the blockchain is valid or not
	##
	def isChainValid(self):
		for i in range (1, self.chain.length):
			currentBlock = self.chain[i]
			prevBlock = self.chain[i-1]
			
			if currentBlock.hash != currentBlock.calculateHash():
				return False
			
			if currentBlock.hash != prevBlock.hash:
				return False
			
			if currentBlock.zipcode != prevBlock.zipcode:
				return False
		
		return True
	
	##
	#   Print the result for all of the blocks in the blockchain to be tested
	#
	#   @param self             The blockchain object to access the attributes within this class
	##
	def printTest(self):
		print('Blockchain Test')
		return self.numBlocks
		
	##
	#   Collect all of the light data from the LDR of each device in the blockchain
	#
	#   @param self             The blockchain object to access the attributes within this class
	##
	def collectChainLightData(self):
		for i in range(0, self.chain.length):
			self.chain{i}.lightData = self.chain[i].getLDR();
	
	##
	#   Collect all of the temp data from the LDR of each device in the blockchain
	#
	#   @param self             The blockchain object to access the attributes within this class
	##
	def collectChainTempData(self):
		for i in range(0, self.chain.length):
			self.chain[i].tempData = self.chain[i].getTemp(4);
	
	##
	#   Calculates the price of all of the blockc within the blockchain for the solar producer
	#
	#   @param self             The blockchain object to access the attributes within this class
	#   
	#   @return                 The price to be sold all of the solar producers within the blockchain
	##
	def calculatePrice(self):
		#checking for sunlight
		self.collectChainLightData();
		minDevices = 1 #needing to find a way to calculate self better
		tally = 0 #keeping track of the number devices detecting sunlight
		isSunlight = False #keeping track if there is sunlight
		for i in range(0, self.chain.length):
			individualLightData = self.chain[i].lightData
			if individualLightData > 50:
				tally += 1
		if tally >= minDevices:
			isSunlight = True #returning a boolean to check if there's sunlight
		
		#calculating price
		if isSunlight == False:
			return 'There is no sunlight, no electricity can be sold'
		else:
			price = 0;
			tempTotal = 0;
			for j in range(0, self.chain.length):
				individualTempData = Number(self.chain[j].tempData)
				tempTotal += individualTempData
				#console.log('TempTotal [', j, ']: ', tempTotal);
				
			tempAvg = Decimal(tempTotal / self.chain.length) #rounding for right now 
			#setting the simplistic price for proof of concept
			#--> will make it more complicated as I work with hardware
			if tempAvg > self.prevTempAvg:
				price = tempAvg * 0.15 #artificial price setting for right now
			else:
				price = tempAvg * 0.10 #artificial price setting for right now
				
			self.prevTempAvg = temp
			return price
	
	##
	#   Makes the transaction from one block to another within the blockchain
	#
	#   @param self             The blockchain object to access the attributes within this class
	#   @param fromAddress      The customer
	#   @param toAddress        The solar producer
	#   @param amount           The amount of the transaction
	##
	def makeTransaction(self, fromAddress, toAddress, amount):
		#checking to see if the address are valid --> DOUBLE SAFEGUARD FEATURE
		self.collectChainLightData();
		isFromAddressValid = False
		isToAddressValid = False
		fromAddressBlockIndex #saving the index to affect the fromAddress block
		toAddressBlockIndex; #saving the index to affect the toAddress block
		for i in range (0, self.chain.length):
			if self.chain[i].index == fromAddress:
				isFromAddressValid = True
				fromAddressBlockIndex = i
			if self.chain[i].index == toAddress:
				isToAddressValid = True
				toAddressBlockIndex = i
				
		#performing the transaction
		if isFromAddressValid == True and isToAddressValid == True: 
			if self.chain[fromAddressBlockIndex].zipcode != self.chain[toAddressBlockIndex].zipcode:
				print('self transaction cannot take place since the zipcodes do not match!')
			if self.chain[toAddressBlockIndex].isSeller == False:
				#cannot sell electricity
				print('The transactoon cannot be made since the money is not going to a solar producer!')
			else:
				#checking for sunlight
				minDevices = 1.5 #needing to find a way to calculate self better
				tally = 0 #keeping track of the number devices detecting sunlight
				isSunlight = False #keeping track if there is sunlight
				
				for i in range(0, self.chain.length):
					individualLightData = Number(self.chain[i].lightData)
					if individualLightData > 50: #voltage condition
						tally += 1
						
				if(tally >= minDevices):
					isSunlight = True #boolean checking for if there is sunlight
				
				if(isSunlight == True):
					if self.chain[fromAddressBlockIndex].balance > amount:
						#transaction can occur
						self.chain[fromAddressBlockIndex].balance -= amount #taking away money from the customer
						self.chain[toAddressBlockIndex].balance += amount #sending the money to the solar producer
						print('Transaction was successful!')
					else:
						print('There is not enough money from the customer for thetransaction to take place!')
				else:
					print('There is no sunlight, so electricity cannot be sold')
		else:
			print('Transaction was not successful due to either one or both addresses are invalid within blockchain!')
	
	##
	#   Gets a balance of one of the block
	#
	#   @param self             The blockchain object to access the attributes within this class
	#   @param address          The block to have its balance display.
	##
	def getBalance(self, address):
		return self.chain[address].balance
	
	##
	#   Print all of the balances of blockchain
	#
	#   @param self             The blockchain object to access the attributes within this class
	##
	def printBalance(self):
		for i in range(0, self.chain.length):
			print('Block Address [', self.chain[i].index , ']: ', self.chain[i].balance)
	
	##
	#   Sends data from one pi to another
	#
	#   @param self             The blockchain object to access the attributes within this class
	##
	def sendData(self):
		UDP_IP = "192.168.1.10" #varying from pi to pi
		UDP_Port = 5005 
		MESSAGE = getMessage(1, 2, False) #changing throughout the demostration to show proof of concept
		#from device 1 to 2
		print("UDP target IP:", UDP_IP)
		print("UDP target port:", UDP_PORT)
		print("message:", MESSAGE)
		sock = socket.socket(socket.AF_INET, # Internet
		socket.SOCK_DGRAM) # UDP
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	
	##
	#   Receives data from one pi to another
	#
	#   @param self             The blockchain object to access the attributes within this class
	##
	def receiveData(self):
		UDP_IP = "192.168.1.45" #varying from pi to pi
		UDP_PORT = 5005
		sock = socket.socket(socket.AF_INET, # Internet
		socket.SOCK_DGRAM) # UDP
		sock.bind(MESSAGE, (UDP_IP, UDP_PORT))
		while True:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		parseAndHandleMessage(data)

	##
	#   Returns a message that needs to be sent
	#
	#   @param self             	The blockchain object to access the attributes within this class
	#   @param fromAddress      	The address that the message is sending from
	#   @param toAddress        	The address that the message is sending to
	#   @param isTransactionMade    A boolean to check if a transaction is made
	##
	def getMessage(self, fromAddress, toAddress, isTransactionMade):
		block_index = self.chain[address].index
		block_zipcode = self.chain[address].zipcode
		block_date = self.chain[address].timestamp
		chain_zipcode = self.chain[0].zipcode #genesis zipcode
		typeOfBlock = self.chain[address].isSeller
		block_balance = self.chain[address].balance
		block_lightData = self.chain[address].lightData
		isBuying = False
		if typeOfBlock == False:
			block_isBuying = True #changing whether the block is a seller or buyer
		
		#parsing for light --> check the voltage of the sensor from the block
		isLightDetected = False
		if block_lightData > 2:
			isLightDetected = True
		
		#checking for the temperature within the device
		temp = getTemp(4); #setting the temperature pin to 4
		
		#displaying the price
		getPrice = self.calculatePrice()
		
		#checking for a transaction --> Commenting this part out for the demo
		amountReceived = 0
		amountSent = 0
		fromAddress = -1 #changing if a transaction is made in demo
		fromAddressStr = ''
		toAddress = -1 #changing if a transaction is made in demo
		toAddressStr = ''
		if isTransactionMade == True:
			#self.makeTransaction(fromAddress, toAddress, getPrice)
			amountReceive = amountReceive + getPrice
			amountSent = amountSent + getPrice
		else:
			fromAddressStr = 'N/A'
			toAddressStr = 'N/A'
		
		#concatenating the string together so the message can be sent
		#only sending relevant information needed to be processed
		MESSAGE = 'Device Address: \t' + str(block_index) + '\n' +
				  'Device Creation Date: \t' + str(block_date) + '\n' +
				  'Device Zip Code: \t' + str(block_zipcode) + '\n' +
				  'Blockchain Zip Code: \t' + str(chain_zipcode) + '\n' +
				  'Is Device from a Producer: \t' + str(block_isBuying) + '\n' +
				  'Voltage Sunlight Detected: \t' + str(block_lightData) + '\n' +
				  'Environmental Temp in C: \t' + str(temp) + '\n' +
				  'Price of the Chain: \t' + str(calculatePrice(self)) + '\n' +
				  'Device Balance: \t' + str(block_balance) + '\n' +
				  'Is Transaction Made: \t' + str(isTransactionMade) + '\n' +
				  'Transaction Came From: \t' + fromAddressStr + '\n' +
				  'Transaction Going To: \t' + roAddressStr + '\n' +
				  'Amount Received \t' + str(amountReceived) '\n' +
				  'Amount Sent \t' + str(amountSent)
				  
		return MESSAGE
	##
	#   Parses and handles a message that needs to be sent
	#
	#   @param data            		The data that needs to be processed
	##
	def parseAndHandleMessage(data):
		#parsing for the important parts of the message
		
		#splitting the message up by '\n' --> need to parse the information in a particular order
		device_address_str, device_zipcode_str, device_date_str,
		blockchain_zipcode_str, device_producer_str, 
		device_lightData_str, device_temp_str, 
		chain_price_str, device_balance_str, isTransactionMade_str, 
		from_address_str, tp_address_str, amount_receive_str, 
		amount_sent_str = data.split('\n')
		
		#parsing for the relevant to handle the message
		device_address = int(device_address_str[-1])
		device_zipcode = int(device_zipcode_str[-1])
		device_date = str(device_date_str[-1])
		blockchain_zipcode = int(blockchain_zipcode_str[-1])
		device_lightData = int(device_lightData_str[-1])
		device_temp = int(device_temp_str[-1])
		chain_price = int(chain_price_str[-1])
		device_balance = int(device_balance_str[-1])
		from_address = int(from_address_str[-1])
		to_address = int(to_address_str[-1])
		amount_receive = int(amount_receive_str[-1])
		amount_sent = int(amount_sent_str[-1])
		
		#parsing for a boolean condition
		isDeviceAProducer = False
		if device_producer_str[-1] == 'True':
			isDeviceAProducer = True
		
		isTransactionMade = False
		transactionAmount = 0
		if isTransactionMade_str[-1] == 'True':
			isTransactionMade = True
			#using this as a double check feature
			if amount_receive == amount_sent:
				transactionAmount = amount_receive
			
		#processing the following information
		#checking, validating, the other information
		#adding the other blocks being received from another device
		#also checking for blockchain validation in this variable
		device_toAddOn = addBlock(new Block(device_address, device_date, isDeviceAProducer, 
											device_temp, device_lightData, device_balance))
	
		print('Is chain valid? ', self.isChainValid()) #checking always for the chain is valid
		#conducting the a transaction when it is made
		if isTransactionMade == True:
			makeTransaction(from_Address, to_Address, transactionAmount)
			#displaying the price of the chain_price
			print('Device # ' + str(self.chain[from_Address], ' : '))
			print('Temp Detected by Device #' + str(self.chain[from_Address]) + 'in C: ' + str(self.chain[from_Address].tempData)) #changing based upon prices
			print('Balance of Device #' + str(self.chain[from_Address]) + ' : $ ' + str(self.chain[from_Address].balance) )#viewing the balance of device
			print('Price of ' + str(self.chain[0].zipcode) + 'per hour: $' + str(self.calculatePrice()))
			#displaying the balance onto the screen for demoing purpose
			print('Transaction Amount: $' + str(amount_receive))
			print('Device # ' + str(self.chain[from_Address]) + '\'s Balance: ' + str(self.chain[from_address].getBalance()))
			print('Device # ' + str(self.chain[to_Address]) + '\'s Balance: ' + str(self.chain[to_address].getBalance()))
		else:
			#displaying the price of the chain_price
			print('Device # ', str(self.chain[from_Address]) + ' : ')
			print('Temp Detected by Device #' + str(self.chain[from_Address]) + 'in C: ' + str(self.chain[from_Address].tempData)) #changing based upon prices
			print('Balance of Device #' + str(self.chain[from_Address]) + ' : $ ' + str(self.chain[from_Address].balance))#viewing the balance of device
			print('Price of ' + str(self.chain[0].zipcode) + 'per hour: $' + str(calculatePrice())) #changing based upon prices

#----------------------------------------------------------------------------------------------------
#Main Area of the console to start running it
			
#starting the chain
solarCoin = Blockchain()
#setting up for the pi device
pi_balance = 100
pi = addBlock(new Block(1, "20/07/2017", "30609", True, 40, 10, device1_balance))

#gathering of the data
solarCoin.collectChainLightData()
solarCoin.collectChainTempData()

#transmitting data 
solarCoin.sendData()
solarCoin.receiveData()
