import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
# Non Android devices will need pyperclip to copy to the clipboard
import pyperclip

# Python for Android:
#   https://python-for-android.readthedocs.io/en/latest/apis/
#   https://github.com/kivy/python-for-android/tree/master
#   https://pypi.org/project/python-for-android/
#   /> pip install python-for-android
#   old: https://anaconda.org/auto/p4a.common
#   
if platform == "android":
  # Get permission to read the filesystem (need to be able to read the key-file)
  from android.permissions import request_permissions, Permission
  request_permissions([Permission.READ_EXTERNAL_STORAGE])
  # Make sure to also have this in the 'buildozer.spec' file:
  #   android.permissions = READ_EXTERNAL_STORAGE
  #
  # We can also manually grant permission to the installed app on the Android device by selecting
  # the app in the system settings and enabling the "Storage" permission.

# The next 7 lines are just so we can import the "secrets" module from this
# directory's parent directory:
import os
import sys
from pathlib import Path

#import inspect
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0, parentdir) 
import secrets


class CiphersApp(App):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.key=""
    self.pwd=""
    self.output=""
    self.home=str(Path.home())


  def btnProcess(self):
    txt=""
    if self.key == "":
      txt="[size=30][color=#FF0000][b]Need an encryption key![/color][/b][/size]\n"
    if self.pwd == "":
      txt=f"{txt}[size=30][color=#FF0000][b]Need a password![/color][/b][/size]"
    if txt != "":
      self.root.ids.lblPwd.text=txt
    else:
      # platform is one of: "android", "linux", "macosx", "ios", "win" or "unknown"
      if platform == "android":
        keyFile=f"{os.environ['EXTERNAL_STORAGE']}/jocreyf.com/secrets/jc_secrets_key.txt"
        print(f"Secondary key file: {keyFile}")
        # log the special key:
        with open(keyFile,"r") as f:
            specialKey=f.readline()
        f.close()
        # Remove potential newline characters from the string:
        specialKey=specialKey.replace("\n", "")
        print(f"Special key: '{specialKey}'")
      else:
        # This will result in looking into the home directory:
        keyFile=""
        print(f"Secondary key file will be searched for in home directory")
      cipher=secrets.AES_256_CBC(key=self.key, keyFile=keyFile, verbose=True)
      print(f"Cipher: {cipher}")
      # Try to decrypt.  If successful, then good.  Otherwise, encrypt.
      try:
        print(f"Trying to decrypt...")
        print(f"  key: '{self.key}'")
        print(f"  pwd: '{self.pwd}'")
        txt=cipher.decrypt(self.pwd)
        print(f"txt: {txt}")
        if txt == "":
          txt="[color=#FF0000]Encrypt returned an empty string.\nThat's not good![/color]"
        else:
          # Looks like the decrypt worked.  Store the decrypted string:
          self.output=txt
      except BaseException as err:
        print(f"decrypt failed: {str(err)}")
        try:
          print(f"Trying to encrypt...")
          print(f"  key: '{self.key}'")
          print(f"  pwd: '{self.pwd}'")
          txt=cipher.encrypt(self.pwd)
          print(f"txt: {txt}")
          if txt == "":
            txt="[color=#FF0000]Decrypt returned an empty string.\nThat's not good![/color]"
          else:
            # Looks like the encrypt worked.  Store the encrypted string:
            self.output=txt
        except BaseException as err:
          print(f"encrypt failed: {str(err)}")
          txt=f"[color=#FF0000]{str(err)}[/color]"

      self.root.ids.lblPwd.text=f"[b]{txt}[/b]"
      # Automatically copy the password on the clipboard so we can paste it:
      try:
        # This will fail in linux:
        Clipboard.copy(txt)
      except:
        # Kivy's clipboard module failed.  Doing it with pyperclip:
        pyperclip.copy(txt)


  def btnClear(self):
    print(f"Clear fields...")
    self.pwd=""
    self.output=""
#    self.root.ids.lblKey.text=""
    self.root.ids.lblPwd.text=""
    self.root.ids.txtPwd.text=""
    self.root.ids.txtPwd.focus=True


  def btnClipboard(self):
    # For some dark reason, Z3 copies only the first 31 characters to the clipboard from a much longer string!!!
    # It works fine on the Samsung S6 though!!!
    print(f"Clip: '{self.output}'")
    try:
      # This will fail in linux:
      Clipboard.copy(self.output)
      print("Clipboard.copy was used")
    except:
      # Kivy's clipboard module failed.  Doing it with pyperclip:
      pyperclip.copy(self.output)
      print("Pyperclip,copy was used")


  def btnExit(self):
    sys.exit(0)


  def txtKey(self):
    self.key=self.root.ids.txtKey.text


  def txtPwd(self):
    self.pwd=self.root.ids.txtPwd.text
#    self.root.ids.lblPwd.text=self.home
# home = "/data" on Android


if __name__ == '__main__':
  CiphersApp().run()
