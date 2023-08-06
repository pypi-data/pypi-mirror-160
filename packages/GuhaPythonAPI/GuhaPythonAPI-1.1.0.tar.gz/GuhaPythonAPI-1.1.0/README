# GuhaAPI

Low Usage Secure Data Encryption Algorithm API, Written in Java, Python, and TypeScript

## Overview

This algorithm allows for an easy way to encrypt and decrypt with a key, while being a low-resource solution, that allows for data privacy on your app. The benefit of this solution is that is doesn't require extra backend resources to run, although it can. The algorithm can also run on the client side. For obvious reasons, this saves money from an infrastructure standpoint, and is easy to integrate with your all of your current data solutions in your app. The only caveat is that all data inputs must be in string formatting and only letters and numbers can be encrypted at this time. The library is written both in TypeScript, Python, and Java for usage across the most popular languages for backend and frontend development. Also, these languages are the most popular for cryptography and much more.

## Information

This algorithm is easy to integrate into your application because the algorithm uses a random key, which provides an added level of security to an already secure cipher. Another added benefit/feature of this approach to encryption is that integration is very simple overall. The entire project is inside of the one TypeScript, Python, and Java files, which makes this very easy to integrate. Make sure to keep the key and the number of times the algorithm has to run on a secure server. This way you can ensure that your data is secure at all times. Additionally, the added benefit of TypeScript, Python, and Java is that they are much safer overall to work with types and such.

## Installation

To install this package you can either copy and paste the code or the guha.ts or guha.py files into your projects, or you can use NPM (Node Package Manager) or the PIP (Python Package Manager) to install this package into your Node.js, Python, or Java project. The NPM, PIP, Maven, and Gradle install commands are below respectively.

```npm install guhaapi```
```pip install GuhaPythonAPI```
```XML
<repositories>
	<repository>
		<id>jitpack.io</id>
		<url>https://jitpack.io</url>
	</repository>
</repositories> 

<dependency>
	<groupId>com.github.yamunasoftware</groupId>
	<artifactId>GuhaAPI</artifactId>
	<version>Tag</version>
</dependency>
```
```Gradle
allprojects {
	repositories {
		maven { url 'https://jitpack.io' }
	}
}

dependencies {
	implementation 'com.github.yamunasoftware:GuhaAPI:Tag'
}
```

If you are working with JavaScript in the web, you can use the UNPKG CDN service. The CDN will deliver the module in a fast and reliable manner, which is preferred for the web. You can get the module using the script tag that is below.

```HTML
<script src="https://unpkg.com/guhaapi" type="module" />
```

## Usage

### Setup

The best way to use this API is to import all of the Guha functions and this declaration will ensure a smooth development process. The JavaScript implementation uses EcmaScript Modules, for your reference. It is beneficial if the class instantiation only takes place once because all of the contents are static. For, Python you should import the package into your project. The best way to declare this object is as follows below in JavaScript Python, and Java respectively. 

```JavaScript
import { Guha } from '.../guha';
``` 
```Python
from guha import Guha
guha = Guha()
```
```Java
import GuhaJavaAPI.Guha;
```

### Key Generation

To use the encryption algorithm, you have to generate a key first using the ```generateKey()``` function and use the resulting key in the encryption method. The function returns a key in the "double" or "float" type and will be used in the encryption process. Make sure to store the key in a secure area, such as a secure server. The other important piece of information that needs to be stored securely is tht number of time the encryption algorithm should run. This should be determined by you, the developer. The more times that the algorithm runs, the more secure the hashed string becomes. The function is listed in JavaScript, Python, and Java respectively.

```JavaScript
Guha.generateKey();
``` 
```Python
guha.generateKey()
```
```Java
Guha.generateKey();
```

### Encryption

The encryption algorithm uses the index of the key and the index of the data. Then, the algorithms uses the key to map the characters to a different value and then uses a block cipher. The cipher is random and uses the key to determine the movement of the blocks. The main point of the key generation is to make sure that it is as hard as possible for hackers to get access to the raw data that is used in the algorithm. That is why we recommend that the encryption key and and the number of times run to be stored in a very secure location, such as a remote server. This will ensure that the encryption algorithm works in the right manner designed. The usage is shown in JavaScript, Python, and Java respectively. Also, the more times the algorithm runs, the more secure it becomes; however, it also uses more resources in the process.

```JavaScript
Guha.encrypt(key, input, times);
```
```Python
guha.encrypt(key, input, times)
```
```Java
Guha.encrypt(key, input, times);
```

### Decryption

The decryption algorithm uses the inverse of the encryption algorithm to reach the same original data that is provided to the algorithm. The decryption algorithm uses the same general security principles as the encryption algorithm and much of the code is actually the exact same, but the key and the number of times ensures the integrity of the algorithm at all times. The usage is shown in JavaScript, Python, and Java respectively.

```JavaScript
Guha.decrypt(key, input, times);
```
```Python
guha.decrypt(key, input, times)
```
```Java
Guha.decrypt(key, input, times);
```

### Tests 

All of the tests are located in the "tests.ts", "tests.py", or "Tests.java" files in the "src/GuhaJavaScriptAPI, src/GuhaPythonAPI, or src/GuhaJavaAPI" directories. There are various tests built into these test files that you can see to verify the validity of the API. Note that if you use the UNPKG service for JavaScript, you will not be able to access the test functions. The usage is in JavaScript, Python, and Java respectively below.

```JavaScript
import * as tests from '.../tests';

console.log(tests.testEncryption(data, times));
console.log(tests.testDecryption(initialData, data, key, times));
console.log(tests.testFullAPI(initialData, times));
```
```Python
import tests

print(tests.testEncryption(data, times))
print(tests.testDecryption(initialData, data, key, times))
print(tests.testFullAPI(initialData, times))
```
```Java
import GuhaJavaAPI.Tests;
...
System.out.println(Tests.testEncryption(data, times));
System.out.println(Tests.testDecryption(initialData, data, key, times));
System.out.println(Tests.testFullAPI(initialData, times));
```