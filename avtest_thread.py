import json
import os.path
from ftplib import FTP
from threading import Thread


class FTPThread(Thread):
    def __init__(self, file_from_json):
        """Инициализация потока"""
        Thread.__init__(self)
        self.file = file_from_json
        self.dest = self.file["to"]
        self.path_to = self.dest["dir"] + self.file["from"]

        self.ftp = FTP()
        self.user = ""
        self.passwd = ""
        self.port = 21

    def __del__(self):
        self.ftp.close()

    def set_from_json(self):
        # Checking port in JSON
        if "port" in self.dest:
            self.port = self.dest["port"]
        # Checking username in JSON
        if "user" in self.dest:
            self.user = self.dest["user"]
        # Checking pass in JSON
        if "pass" in self.dest:
            self.passwd = self.dest["pass"]

    def run(self):
        self.set_from_json()

        info = "From: " + self.file["from"] + "\t"
        info += "\tTo: " + "ftp://" + self.dest["server"] + "/" + self.dest["dir"] + "\n"
        info += self.ftp.connect(self.dest["server"], self.port) + "\n"
        info += self.ftp.login(self.user, self.passwd) + "\n"

        with open(self.file["from"], 'rb') as fobj:
            info += self.ftp.storbinary('STOR ' + self.path_to, fobj, 1024)
            info += "\nFile size: " + str(os.path.getsize(self.file["from"])) + " bytes\n"

        print(info)


def main(json_file):
    # Reading JSON file in data
    with open(json_file, "r") as read_file:
        data = json.load(read_file)
        files = data["files"]

    # Print and upload all copying files in JSON
    print("\n\n Copying files:\n")
    for f in files:
        my_thread = FTPThread(f)
        my_thread.start()


if __name__ == "__main__":
    json_f = "data.json"
    main(json_f)
