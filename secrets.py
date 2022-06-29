#!/usr/bin/env python3
# ======================================================================================================== #
# Little app to encrypt/decrypt strings using a standard, strong cipher (AES 256bit).                      #
# You can set a string (key) to encrypt the text with.  A blank, empty string is accepted too in case      #
# that's what's wanted.                                                                                    #
# The tool also supports an extra optional key string that is stored in a text file.  This extra key will  #
# be combined with the primary key string to provide a little extra security.                              #
# (default location of optional "extra" key-file: ~/jc_secrets_key.txt)                                    #
# (the path to the extra key-file can be overridden by setting env variable: 'JC_SECRETS_FILE')            #
#                                                                                                          #
# Arguments:                                                                                               #
#    --version                         : show app version                                                  #
#    -v          | --verbose           : show verbose level output                                         #
#    -e          | --encrypt           : encrypt the string                                                #
#    -d          | --decrypt           : decrypt the string                                                #
#    -k <string> | --key <string>      : encryption key                                                    #
#                                        can also be set through environment variable 'JC_SECRETS_KEY'     #
#    -p <string> | --password <string> : the string to encrypt/decrypt                                     #
#    -f <uri>    | --file <uri>        : file to process html <PWD>-tags                                   #
#                                                                                                          #
# Example:                                                                                                 #
#   /> $0 -k MyKey -e -p MySecret                                                                          #
#      -> bjJxQ2VxVzRRNEMyeXVyRXFJR2k5clpDMlNaSldWc1AyOU5DS3dkQmJ3Zz0=                                     #
#                                                                                                          #
#   /> export JC_SECRETS_KEY="MyKey"                                                                       #
#   /> export JC_SECRETS_FILE=~/jc_secrets_key.txt                                                         #
#   /> $0 -d -p bjJxQ2VxVzRRNEMyeXVyRXFJR2k5clpDMlNaSldWc1AyOU5DS3dkQmJ3Zz0=                               #
#      -> MySecret                                                                                         #
# -------------------------------------------------------------------------------------------------------- #
# We're using this Crypto implementation for the AES 256bit CBC cipher logic:                              #
#   https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256                    #
#                                                                                                          #
#   pip install pycryptodome                                                                               #
# or                                                                                                       #
#   conda install pycryptodome                                                                             #
# ======================================================================================================== #
#  2021-11-20  v0.1  jcreyf  Initial version.                                                              #
#  2022-06-28  V0.2  jcreyf  Fix issue with encryption key and simplify things.                            #
# ======================================================================================================== #
import os
import base64
import hashlib
from pathlib import Path    # Needed to find the home directory of the user
from Crypto import Random
from Crypto.Cipher import AES

class AES_256_CBC(object):
    """ This class will encrypt/decrypt using the aes-256-cbc cipher.
    """
    __version__ = "v0.2 - 2022-06-28"
# ToDo: Add a tag in front and at the end of the encoded string.  We can use those tags later in more complicated search filter.
#    __pretag__  = "JC22#"
#    __posttag__ = "#JC22"

    @staticmethod
    def version() -> str:
        """ Static app version details """
        return f"{os.path.basename(__file__)}: {AES_256_CBC.__version__}"


    def __init__(self, key: str = "", keyFile: str = "", verbose: bool = True) -> None:
        """ Constructor, setting the encryption key.
        If we have a secondary "special key" on the system, then that secondary key
        will be used to encrypt the encryption key.  That encrypted key then becomes the
        actual key to encrypt and decrypt secrets.

        Arguments:
            key (str): the encryption key;
            keyFile (str): the full path to a file that has the optional secondary encryption key;
            verbose (bool): level of log messages;
        """
        self._verbose=verbose
        self._key_hash=None
        self._key=None
        self._key_file=None
        self._special_key=False
        self._block_size=AES.block_size
        # We may have gotten the default, empty-string encryption key.  See if a key was set in the
        # environment variable and use that if set:
        if key == "":
            try:
                key=os.environ['JC_SECRETS_KEY']
            except KeyError:
                # Environment variable has not been set.  Ignore the issue and use the default emty string.
                pass

        # Set the secondary optional "special key" (if we have one):
        try:
            if keyFile == "":
                # Get the path from the 'JC_SECRETS_FILE' environment variable (if set):
                try:
                    keyFile=os.environ["JC_SECRETS_FILE"]
                except KeyError:
                    # We get this exception if the environment variable is not set.
                    # Try the home directory if no explicit directory was given:
                    keyFile=f"{str(Path.home())}/jc_secrets_key.txt"

#            self.log(f"Extra key: {keyFile}")
            with open(keyFile,"r") as f:
                specialKey=f.readline()
            f.close()
            # Remove potential newline characters from the string:
            specialKey=specialKey.replace("\n", "")
            self._key_file=keyFile
        except:
            # Ignore any and all exceptions to truly make the "special key" optional.
            specialKey=""

        if specialKey == "":
            # Use the given key if we don't have a "special key":
            self._key=key
            self._key_hash=hashlib.sha256(self._key.encode()).digest()
        else:
            # Aha!  We have a secondary key to make things a little bit more "special".
            self._key=f"{specialKey}#{key}"
            self._key_hash=hashlib.sha256(self._key.encode()).digest()
            self._special_key=True
            self.log("Extra key set")


    @property
    def key(self) -> str:
        return self._key


    @property
    def special_key(self) -> bool:
        return self._special_key


    @property
    def key_file(self) -> str:
        return self._key_file


    def log(self, msg: str) -> None:
        """ Method to log messages.

        Arguments:
            msg (str): the message to log
        """
        if self._verbose:
            print(msg)


    def encrypt(self, txt: str) -> str:
        """ Encrypt a string and return it as a Base64 encoded string.

        Arguments:
            txt (str): the string to encrypt;

        Returns:
            str: the return value is a Base64 encoded string;

        Raises:
            multiple potential exceptions during either the encryption or encoding process;
        """
        # Make sure the text is at the correct length:
        txt=AES_256_CBC.__pad(txt, blockSize=self._block_size)
        # Generate a random seed based on AES block size (16 bytes in our case):
        iv=Random.new().read(self._block_size)
        # Initialize the cipher:
        cipher=AES.new(self._key_hash, AES.MODE_CBC, iv)
        encoded=base64.b64encode(iv+cipher.encrypt(txt.encode()))
        # We now have a byte object with the encrypted string.
        # Encode it as Base64:
        encoded=base64.b64encode(encoded)
        # Return it as a string:
        return encoded.decode("utf-8")


    def decrypt(self, txt: str) -> str:
        """ Decrypt a string

        Arguments:
            txt (str): the string to decrypt;

        Returns:
            str: the return value is the decrypted string;

        Raises:
            multiple potential exceptions during either the decoding or decryption process;
        """
        txt_bytes=txt.encode("utf-8")
        decode_bytes=base64.b64decode(txt_bytes)
        decode_txt=decode_bytes.decode("utf-8")
        txt=base64.b64decode(decode_txt)
        iv=txt[:AES.block_size]
        cipher=AES.new(self._key_hash, AES.MODE_CBC, iv)
        decrypt_txt=AES_256_CBC.__unpad(cipher.decrypt(txt[AES.block_size:]))
        return decrypt_txt.decode('utf-8')


    @staticmethod
    def __pad(txt: str, blockSize: int) -> str:
        """ Append characters to the string to make sure it's the correct length for the block size in the AES encryption.

        Arguments:
            txt (str): the text to pad
            blockSize (int): the number of characters needed in the unicode block

        Returns:
            str: the padded text
        """
        return txt + \
            (blockSize - len(txt) % blockSize) * \
            chr(blockSize - len(txt) % blockSize)


    @staticmethod
    def __unpad(txt: str) -> str:
        """ Remove the extra characters (if any) that were added during the encryption process.
        """
        return txt[:-ord(txt[len(txt)-1:])]

# ------

if __name__ == "__main__":
    import sys
    import argparse
    from bs4 import BeautifulSoup

    VERBOSE=False
    def verbose(str):
        """ Only print the message if the Verbose-flag is set. """
        if VERBOSE:
            print(str)

    def processFile(file, encode=True):
        """ Method to encrypt or decrypt all values between <PWD> tags in some HTML-file. """
        print(f"Processing file: {file}")
        # This works to find all passwords (between <PWD> tags):
        html = BeautifulSoup(open(file).read(), "html.parser")
        # Loop through them all:
        for pwd in html.findAll("pwd"):
            txt=pwd.contents[0]
            verbose(f"'{txt}' on line: {pwd.sourceline}, col: {pwd.sourcepos}")
            if encode:
                secret=cipher.encrypt(txt)
            else:
                secret=cipher.decrypt(txt)
            verbose(f" {txt}  ->  {secret}")
            new_tag=html.new_tag("PWD")
            new_tag.string=secret
            pwd.replace_with(new_tag)
        # Write the new html doc:
        new_file=f"{file}_new.html"
        print(f"Writing updates to: {new_file}")
        f=open(new_file, "w")
        f.write(str(html))
        f.close()


    # Define the command-line arguments that the app supports:
    parser=argparse.ArgumentParser(description="Encrypt or Decrypt secrets.", \
                                   epilog=f"example: %(prog)s -e -k 'MyKey' -p 'MySecret'")
    parser.add_argument("--version", \
                        action="version", \
                        version=AES_256_CBC.version())
    parser.add_argument("-v", "--verbose", \
                        dest="__VERBOSE", \
                        required=False, \
                        default=False, \
                        action="store_true", \
                        help="show verbose level output")
    parser.add_argument("-e", "--encrypt", \
                        dest="__ENCRYPT", \
                        required=False, \
                        default=False, \
                        action="store_true", \
                        help="encrypt the string")
    parser.add_argument("-d", "--decrypt", \
                        dest="__DECRYPT", \
                        required=False, \
                        default=False, \
                        action="store_true", \
                        help="decrypt the string")
    parser.add_argument("-k", "--key", \
                        dest="__KEY", \
                        required=False, \
                        metavar="<string>", \
                        help="encryption key (you can also set env var 'JC_SECRETS_KEY')")
    parser.add_argument("-p", "--password", \
                        dest="__PWD", \
                        required=False, \
                        metavar="<string>", \
                        help="the string to encrypt/decrypt")
    parser.add_argument("-f", "--file", \
                        dest="__FILE", \
                        required=False, \
                        metavar="<file uri>", \
                        help="file to process html <PWD>-tags")

    # Now parse the command-line arguments and automatically take care of handling some of the usage requests:
    __ARGS=parser.parse_args()

    # Pull out the values that we want:
    VERBOSE=__ARGS.__VERBOSE
    ENCRYPT=__ARGS.__ENCRYPT
    DECRYPT=__ARGS.__DECRYPT
    pwd=__ARGS.__PWD
    key=__ARGS.__KEY
    file=__ARGS.__FILE

    # Display version information (if the verbose flag is set):
    verbose(AES_256_CBC.version())

    # Do some argument validations:
    if (ENCRYPT or DECRYPT)==False:
        sys.exit("Need to use the '-e' (encrypt) or '-d' (decrypt) flag!")
    if (ENCRYPT and DECRYPT)==True:
        sys.exit("Can't use both the '-e' (encrypt) and '-d' (decrypt) flags at the same time!")
    if pwd == None and __ARGS.__FILE == None:
        sys.exit("Need to provide a password (-p) or file (-f) to process!")
    if pwd != None and __ARGS.__FILE != None:
        sys.exit("Can't provide both a password (-p) and a file (-f) to process at the same time!")
    # The encryption key can be set through the '-k' argument on the command line or through the 'JC_SECRETS_KEY' env var.
    # It's not optional though, so we need a value one way or the other! (an explicit empty string is accepted)
    if key == None:
        try:
            key=os.environ['JC_SECRETS_KEY']
        except KeyError:
            sys.exit("Need to use '-k' flag to provide an encryption key or set it through the 'JC_SECRETS_KEY' environment variable!")

    # Instantiate our encryption object:
    cipher=AES_256_CBC(key=key, verbose=VERBOSE)

    if file != None:
        # We need to process a file:
        processFile(file, ENCRYPT)
    else:
        # No file processing.  Just a single encrypt/decrypt:
        if ENCRYPT:
            print(cipher.encrypt(pwd))
        else:
            try:
                secret=cipher.decrypt(pwd)
                # We may get an empty decrypted string if for example a secondary key was used to generate the
                # encrypted string and are now trying to decrypt without that secondary key!
                if secret != "":
                    print(secret)
                else:
                    sys.exit("The secret decrypted into an empty string!")
            except BaseException as err:
                sys.exit(f"Failed to decrypt!!! -> {str(err)} ({err.__class__})")