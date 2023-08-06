# entity-everything
![CI](https://github.com/danrog303/entity-everything/actions/workflows/build.yml/badge.svg)
![Activity](https://shields.io/github/last-commit/danrog303/entity-everything)
>  Easy to use tool for encoding text to html entities and html entities to normal text. 

## ✨ Features
1. Encoding & decoding of text passed as an argument
2. Encoding & decoding of text from the standard input

## 📝 Project description
There are plenty of online tools on the Internet for encoding text to html entities. However, the solutions i found have one thing in common: they only convert special characters, without changing letters and numbers.

If for some reason you want to convert letters and numbers to entities as well, "entity-everything" is the script for you.

## 💻 How to download?
Project is available on PyPi, so you can install entity-everything using pip:
```
$ python -m pip install entity_everything
```


## 🔧 How to use?
1️⃣ Encoding text:
```
$ python -m entity_everything encode "Text to encode"
or
$ echo "Text to decoode" | python -m entity_everything encode
```
```
Result: "&#84;&#101;&#120;&#116;&#32;&#116;&#111;&#32;&#101;&#110;&#99;&#111;&#100;&#101;"
```
2️⃣ Decoding text:
```
$ python -m entity_everything decode "&#120;&#120;&#120;"
or
$ echo "&#120;&#120;&#120;" | python -m entity_everything decode
```
```
Result: "xxx"
```


## ⚙️Technologies used
The script has been written in Python.
It should work with versions 3.9 or higher.
This script does not require any dependencies.
