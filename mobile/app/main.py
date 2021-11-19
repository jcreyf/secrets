#
# THIS FILE IS AN EXACT COPY OF secrets.py!!!!
# THIS FILE IS REQUIRED FOR BUILDOZER TO GENERATE THE ANDROID APP
#
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.core.clipboard import Clipboard

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
    self.home=str(Path.home())


  def btnProcess(self):
    cipher=secrets.AES_256_CBC(self.key)
    txt=cipher.encrypt(self.pwd)
    self.root.ids.lblPwd.text=txt
    # Automatically copy the password on the clipboard so we can paste it:
    Clipboard.copy(txt)


  def txtKey(self):
    self.key=self.root.ids.txtKey.text


  def txtPwd(self):
    self.pwd=self.root.ids.txtPwd.text
    self.root.ids.lblPwd.text=self.home


if __name__ == '__main__':
  CiphersApp().run()
