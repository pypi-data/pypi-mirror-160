from guha import Guha

# GUHA API TEST OBJECTS  #

# Guha Class Object Declaration:
guha = Guha()

# GUHA API TEST FUNCTIONS #

# Test Full API Function:
def testFullAPI(initialData: str, times: int):
  # Performs the API Test:
  key: float = guha.generateKey()
  data: str = guha.encrypt(key, initialData, times)

  # Checks the Case:
  if guha.decrypt(key, data, times) == initialData:
    # Returns the Truth Value:
    return True
  
  else:
    # Returns the Truth Value:
    return False

# Encryption Test Function:
def testEncryption(data: str, times: int):
  # Tests the Encryption:
  return guha.encrypt(guha.generateKey(), data, times)

# Decryption Test Function:
def testDecryption(initialData: str, data: str, key: float, times: int):
  # Tests the Decryption:
  if initialData == guha.decrypt(key, data, times):
    # Returns the Truth Value:
    return True
  
  else:
    # Returns the Truth Value:
    return False