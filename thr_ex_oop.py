import json
import os.path
from ftplib import FTP
from threading import Thread


class FTPThread(Thread):
    def __init__(self, file_from_json):

        if file_from_json is None:
            raise Exception(AttributeError, "File in JSON is empty!!!")

        """Инициализация потока"""
        Thread.__init__(self)

        self.ftp = FTP()

        self.user = ""
        self.passwd = ""
        self.port = 21

        self.file = file_from_json
        self.dest = self.file["to"]
        self.path_to = self.dest["dir"] + self.file["from"]

    def __del__(self):
        self.ftp.close()

    def _set_from_json(self):

        # Checking port in JSON
        if "port" in self.dest:
            self.port = self.dest["port"]

            if self.port is None:
                raise Exception(AssertionError, "Port not initialized!!!")
            if self.port is 0:
                raise Exception(AssertionError, "Port empty!!!")

        # Checking username in JSON
        if "user" in self.dest:
            self.user = self.dest["user"]

            if self.user is None:
                raise Exception(AssertionError, "User not initialized!!!")
            if self.user is "":
                raise Exception(AssertionError, "User empty!!!")

        # Checking pass in JSON
        if "pass" in self.dest:
            self.passwd = self.dest["pass"]

            if self.passwd is None:
                raise Exception(AssertionError, "Pass not initialized!!!")
            if self.passwd is "":
                raise Exception(AssertionError, "Pass empty!!!")

    def run(self):
        self._set_from_json()

        info = "From: " + self.file["from"] + "\t"
        info += "\tTo: " + "ftp://" + self.dest["server"] + "/" + self.dest["dir"] + "\n"
        info += self.ftp.connect(self.dest["server"], self.port) + "\n"
        info += self.ftp.login(self.user, self.passwd) + "\n"

        try:
            fobj = open(self.file["from"], 'rb')
        except AttributeError as e:
            print(u'Couldn\'t open file!!!' )
        else:
            with fobj:
                info += self.ftp.storbinary('STOR ' + self.path_to, fobj, 1024)
                info += "\nFile size: " + str(os.path.getsize(self.file["from"])) + " bytes\n"

        print(info)


def main(json_file):

    try:
        f_json = open(json_file, "r")
    except IOError as e:
            print(u'Couldn\'t open JSON file!!!')
    else:
        with f_json:
            # Reading JSON file in data
            data = json.load(f_json)
            files = data["files"]

    # Print and upload all copying files in JSON
    print("\n\n Copying files:\n")
    for f in files:
        my_thread = FTPThread(f)
        my_thread.start()


if __name__ == "__main__":
    json_f = "data.json"
    main(json_f)
