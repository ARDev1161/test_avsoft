import json
import os.path
from ftplib import FTP

ftp = FTP()

last_dest = ""
count = 0


# Reading JSON file in data
with open("data.json", "r") as read_file:
    data = json.load(read_file)

# Copying "files"
files = data["files"]

# Print and upload all copying files in JSON
print("\n\n Copying files:\n")
for f in files:
    user = ""
    passwd = ""

    port = 21
    dest = f["to"]

    print("From: " + f["from"] + "\t\tTo: " + "ftp://" + dest["server"] + "/" + dest["dir"])

    # Checking port in JSON
    if "port" in dest:
        port = dest["port"]
    # Checking username in JSON
    if "user" in dest:
        user = dest["user"]
    # Checking pass in JSON
    if "pass" in dest:
        passwd = dest["pass"]

    if dest["server"] != last_dest:
        if count != 0:
            print(ftp.close())
        print(ftp.connect(dest["server"], port))
        print(ftp.login(user, passwd))
    else:
        print("Using the same repository.")


    path_to = dest["dir"] + f["from"]
    with open(f["from"], 'rb') as fobj:
        print(ftp.storbinary('STOR ' + path_to, fobj, 1024))

    print("File size: " + str(os.path.getsize(f["from"])) + " bytes\n")

    count += 1
    last_dest = dest["server"]
ftp.close()
