## Description

Simple python script that will open and initialize the download of all the ids for VR videos inside a file called ids.txt, after the download it's started it will stop it automatically and import the URL inside a txt, those URLs can be used on any download manager, like jDownloader2, to bulk donwload VR videos from DMM, those videos will be encrypted so you need a software like jav-it to decrypt it, or you can view the files using DMM Video Player.

## Installation for the script
1. Install the latest python version from: 
https://www.python.org/downloads/ (tick add to PATH option)
2. Install the playwright using:
pip install playwright
and
playwright install
3. Open the script and change:
email = "EMAIL"
password = "PASSWORD"
edit it with your actual DMM email and password, don't remove the quotations, and edit only the text inside the quotation, save the file.
4. Insert the ids you want to download from DMM inside a txt file in the same folder called ids.txt, is suggested to put max 50 IDS x batch.
5. Run the script using: 
    python VRGen.py
6. After the batch is done use something like jDownload2 (https://jdownloader.org/jdownloader2) to add all the URLs from the newly generated file: vrUrls.txt, the URLs have a validity of 8/12 hours, so download them before they expire, or you will need to generate them again.

### License
    GNU GPLv3
