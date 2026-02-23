import struct
import os
import json # Ненавижу джисон
import typing
import pickle
from importlib import resources

"""
JLDI - Just Little Dumb Idea
"""

class JLDI:
    IdentifierA= b"JLDI_V01"
    HeaderA= 32
    SizeA= 8

    def __init__(self,filename: str): self.filename= filename
    def __get_type__(self, extension: str) -> str:
        image, audio, text = {'.png'}, {'.mp3'}, {'.txt'}
        ext = extension.lower()
        if ext in image: return 'image'
        elif ext in audio: return 'audio'
        elif ext in text: return 'text'
        else: return 'binary'
    def create(self,metadata: typing.Dict[str, typing.Any], python_code: str, resources: typing.Dict[str, bytes]) -> None:
        metadata= json.dumps(metadata, ensure_ascii=False).encode("utf-8")
        pythonPiece= python_code.encode("utf-8")
        temp={}
        for title, data in resources.items():
            ext= os.path.splitext(title)[1].lower()
            temp[title]= { 'data': data, 'type': self.__get_type__ }
        cucumber = pickle.dumps(temp)


        offset= {
            'metadata': self.SizeA+self.HeaderA,
            'py': self.SizeA+self.HeaderA+len(metadata),
            'resources': self.SizeA+self.HeaderA+len(pythonPiece)+len(metadata)
        }

        header= struct.pack(
            '!QQQQ',
            offset['metadata'],
            len(metadata),
            len(pythonPiece),
            len(cucumber),
        )

        with open(self.filename, "wb") as f:
            f.write(self.IdentifierA)
            f.write(header)
            f.write(metadata)
            f.write(pythonPiece)
            f.write(cucumber)
    def read(self) -> typing.Tuple[typing.Dict[str, typing.Any], str, typing.Dict[str, bytes]]:
        if not os.path.exists(self.filename): raise FileNotFoundError(f"Pff...Wrong path, I can't found {self.filename}. U~U")
        with open(self.filename, "rb") as f:
            if f.read(self.SizeA) != self.IdentifierA: raise ValueError(f"That wro-o-o-ong. I need {self.IdentifierA}, not {self.SizeA}. >:[")
            if len(f.read(self.HeaderA)) != self.HeaderA: raise ValueError("Ouch!!! It hurts..I'm damaged... >~<")
            metadata_offset, metadata_size, python_size, resources_size= struct.unpack('!QQQQ', f.read(self.HeaderA))

            f.seek(metadata_offset); metadata_bytes= f.read(metadata_size)
            try: metadata= json.loads(metadata_bytes.decode("utf-8"))
            except json.decoder.JSONDecodeError as e: raise ValueError(f"Sorry...I can't read it... >~<")

            python_bytes= f.read(python_size)
            try: python_code= python_bytes.decode("utf-8")
            except UnicodeDecodeError as e: raise ValueError(f"Sorry...I can't read it... >~<")

            resources_bytes= f.read(resources_size)
            try: resources_serialized= pickle.loads(resources_bytes)
            except Exception as e: raise ValueError(f"Sorry...I can't read it... >~<")

            temp={}
            for name, res_data in resources_serialized.items(): temp[name]= res_data['data']
            return metadata, python_code, temp
    def get_metadata(self) -> typing.Dict[str, typing.Any]:
        with open(self.filename, "rb") as f: f.seek(self.SizeA); header_data= f.read(self.HeaderA); metadata_offset, metadata_size, _, _ = struct.unpack('!QQQQ', header_data); f.seek(metadata_offset); return json.loads(f.read(metadata_size).decode("utf-8"))
    def extract_python_code(self, output_file: typing.Optional[str] = None) -> str:
        _, python_code, _= self.read()
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f: f.write(python_code)
