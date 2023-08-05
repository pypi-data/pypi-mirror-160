import io
import os
from amulet_nbt import *


class DummyFile:
    """
    A dummy file made to work with Amulet_NBT.
    """

    def __init__(self, contents=None):
        """
        Initialize with contents
        """
        self.contents = contents

    def write(self, to_write):
        """
        Replace contents with to_write.
        """
        self.contents = to_write


class LevelFile:
    """
    Wrapper around TextIOWrapper for interacting with entity data files.
    """

    def __init__(self, file_=None):
        """
        Initialize the file.
        file_ can be anything as long as it provides read(bytes) and the string variable file_.name.
        If the file is empty or is None, a dummy file will be created.
        The NBT data is stored in self.contents, and is a NBTFile, from amulet_nbt. For more information see amulet_nbt's documentation.
        """

        if  file_ == None or os.path.getsize(file_.name) == 0:
            self.contents = NBTFile(
                value=TAG_Compound(
                    {}
                )
            )
        else:
            self.contents_raw = file_.read()[8:]
            #print(self.contents_raw)
            #print(self.header_length)
            #print(self.header_constant)
            self.contents = load(
                self.contents_raw, little_endian=True, compressed=False
            )

    def save(self, file_):
        """
        Saves into the specified file_
        file_ can be anything providing write(data)
        This automatically adds the header.
        """
        dummy = DummyFile()
        self.contents.save_to(dummy, little_endian=True, compressed=False)
        contents = b'\x03\x00\x00\x00'
        contents += len(dummy.contents).to_bytes(4, "little")
        contents += dummy.contents
        file_.write(contents)
