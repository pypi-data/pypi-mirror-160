import array
import math
import random

class Guha:
  # ENCRYPTION ALGORITHM VARIABLES #

  # Possible Values Array:
  possibleValues: array = [
    "A", "B", "C", "D", "E",
    "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y",
    "Z",

    "a", "b", "c", "d", "e",
    "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y",
    "z",

    "0", "1", "2", "3", "4",
    "5", "6", "7", "8", "9",

    "!", "@", "#", "$", "%",
    "^", "&", "*", "(", ")",
    "<", ">", "?", "/", "'",
    ":", ";", "[", "]", "{",
    "}", "|", " "
  ]

  # ENCRYPTION ALGORITHM FUNCTIONS #

  # Generate Key Function:
  def generateKey(self):
    # Returns the Key:
    return ((random.random() * 0.9) + 0.1)

  # Encryption Function:
  def encrypt(self, key: float, input: str, times: int):
    # Loop Variables:
    outputString: str = input
    holderString: str = ""
    turns: int = 0

    # Loops through Times:
    while turns < times:
      # Gets the Output:
      holderString = self.encryptionOperation(key, outputString)
      outputString = holderString
    
      turns+=1

    # Returns the Output:
    return outputString

  # Decryption Function:
  def decrypt(self, key: float, input: str, times: int):
    # Loop Variables:
    outputString: str = input
    holderString: str = ""
    turns: int = 0

    # Loops through Times:
    while turns < times:
      # Gets the Output:
      holderString = self.decryptionOperation(key, outputString)
      outputString = holderString

      turns+=1

    # Returns the Output:
    return outputString

  # Encryption Operation Function:
  def encryptionOperation(self, key: float, input: str):
    # Loop Variables:
    outputArray: array = list(input)
    index: int = math.floor(key * len(outputArray))
    turns: int = 0

    # Loops through Array:
    while turns < len(outputArray):
      # Swaps the Values:
      value: str = outputArray[turns]
      outputArray[turns] = outputArray[index]
      outputArray[index] = value

      turns+=1

    # Returns the String:
    return self.hashData(key, "".join(outputArray))

  # Decryption Operation Function:
  def decryptionOperation(self, key: float, input: str):
    # Loop Variables:
    newInput: str = self.rehashData(key, input)
    outputArray: array = list(newInput)
    index: int = math.floor(key * len(outputArray))
    turns: int = len(outputArray) - 1

    # Loops through Array:
    while turns >= 0:
      # Swaps the Values:
      value: str = outputArray[index]
      outputArray[index] = outputArray[turns]
      outputArray[turns] = value
    
      turns-=1

    # Returns the String:
    return "".join(outputArray)

  # Hash Data Function:
  def hashData(self, key: float, data: str):
    # Loop Variables:
    hashedData: str = ""
    turns: int = 0

    # Loops through String:
    while turns < len(data):
      # Checks the Case:
      if self.checkInputValues(data[turns]) != -1:
        # Gets the Data Indexes:
        dataIndex: int = self.checkInputValues(data[turns])
        keyTurns: int = math.floor(key * len(self.possibleValues))
        newIndex = dataIndex + keyTurns

        # Checks the Case:
        if newIndex >= len(self.possibleValues):
          # Sets the New Index:
          newIndex -= len(self.possibleValues)

        # Sets the New Value:
        hashedData += self.possibleValues[newIndex]
    
      else:
        # Adds the Data:
        hashData += data[turns]

      turns+=1
  
    # Returns the Hashed Data:
    return hashedData

  # Rehash Data Function:
  def rehashData(self, key: float, data: str):
    # Loop Variables:
    rehashedData: str = ""
    turns: int = 0

    # Loops through String:
    while turns < len(data):
      # Checks the Case:
      if self.checkInputValues(data[turns]) != -1:
        # Gets the Data Indexes:
        dataIndex: int = self.checkInputValues(data[turns])
        keyTurns: int = math.floor(key * len(self.possibleValues))
        newIndex = dataIndex - keyTurns

        # Checks the Case:
        if newIndex < 0:
          # Sets the New Index:
          newIndex += len(self.possibleValues)

        # Sets the New Value:
        rehashedData += self.possibleValues[newIndex]

      else:
        # Adds the Data:
        rehashData += data[turns]

      turns+=1

    # Returns the Rehashed Data:
    return rehashedData

  # Check Input Values Function:
  def checkInputValues(self, input: str):
    # Loop Variables:
    index: int = -1
    turns: int = 0

    # Loops through Array:
    while turns < len(self.possibleValues):
      # Checks the Case:
      if input == self.possibleValues[turns]:
        # Sets the Index
        index = turns
        break

      turns += 1
  
    # Returns the Index:
    return index