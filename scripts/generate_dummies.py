import os
import bcrypt
from passlib.hash import md5_crypt, sha512_crypt
import hashlib
from pathlib import Path

Path("data").mkdir(exist_ok=True)

with open("data/dummy_shadow.txt", "w") as f:
    f.write("alice:" + md5_crypt.hash("password", salt="salt1234") + ":19468:0:99999:7:::\n")
    f.write("bob:" + bcrypt.hashpw(b"qwerty", bcrypt.gensalt()).decode() + ":19468:0:99999:7:::\n")
    f.write("admin:" + sha512_crypt.hash("123456") + ":19468:0:99999:7:::\n")

from passlib.hash import nthash

ntlm = nthash.hash("password")
with open("data/dummy_pwdump.txt", "w") as f:
    f.write(f"Administrator:500:aad3b435b51404eeaad3b435b51404ee:{ntlm}:::\n")
    f.write("Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\n")
