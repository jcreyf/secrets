#
# THIS FILE IS AN EXACT COPY OF secrets.py!!!!
# THIS FILE IS REQUIRED FOR BUILDOZER TO GENERATE THE ANDROID APP
#
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
# Non Android devices will need pyperclip to copy to the clipboard
import pyperclip

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
        keyDir="/storage/emulated/0/jocreyf.com/secrets"
      else:
        # This will result in looking into the home directory:
        keyDir=""
      print(f"Secondary key file: {keyDir}/key.txt")
      cipher=secrets.AES_256_CBC(key=self.key, keyDir=keyDir, verbose=True)
      print(f"Cipher: {cipher}")
      # Try to decrypt.  If successful, then good.  Otherwise, encrypt.
      try:
        print(f"Trying to decrypt...")
#        print(f"  key: '{self.key}'")
#        print(f"  pwd: '{self.pwd}'")
        txt=cipher.decrypt(self.pwd)
#        print(f"txt: {txt}")
        if txt == "":
          txt="[color=#FF0000]Encrypt returned an empty string.\nThat's not good![/color]"
        else:
          # Looks like the decrypt worked.  Store the decrypted string:
          self.output=txt
      except BaseException as err:
        print(f"decrypt failed: {str(err)}")
        try:
          print(f"Trying to encrypt...")
#          print(f"  key: '{self.key}'")
#          print(f"  pwd: '{self.pwd}'")
          txt=cipher.encrypt(self.pwd)
#          print(f"txt: {txt}")
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
    try:
      # This will fail in linux:
      Clipboard.copy(self.output)
    except:
      # Kivy's clipboard module failed.  Doing it with pyperclip:
      pyperclip.copy(self.output)


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
