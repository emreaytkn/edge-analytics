import io
from avro.io import DatumReader, BinaryDecoder
from avro.schema import parse


class DecoderFactory:
    """Factory class for the decoders"""


    @staticmethod
    def get_decoder(input_format, data_schema):
        if input_format == 'RAW':
            raise Exception("Not implemented")
        elif input_format == 'AVRO':
            return AvroDecoder(data_schema)
        elif input_format == 'JSON':
            raise Exception("Not implemented")
        else:
            raise ValueError(input_format)
            
class AvroDecoder:
    def __init__(self, data_schema):
        self.data_schema = open(data_schema, "r").read()
        self.avro_data_schema = parse(self.data_schema)
    

    # Decode messages
    def avro_decoder(self, msg_value, reader):

        message_bytes = io.BytesIO(msg_value)

        decoder = BinaryDecoder(message_bytes)
        event_dict = reader.read(decoder)
        return event_dict
    
    def decode(self, x):
        reader_x = DatumReader(self.avro_data_schema)

        decode_x = self.avro_decoder(x, reader_x)

        res= []
        for key in decode_x.keys():
            res.append(decode_x.get(key))
        

        return res