import grpc

from dataclasses import dataclass, field
from typing import Any

from .. import lightning_pb2 as ln
from .. import lightning_pb2_grpc as lnrpc



@dataclass(frozen=True)
class LightningService:
    host: str
    port: str
    cert: bytes
    macaroon: bytes

    lightning_stub: field(init=False)

    def __post_init__(self):

        def metadata_callback(context, callback):
            callback([("macaroon", self.macaroon)], None)

        cert_creds = grpc.ssl_channel_credentials(self.cert)
        auth_creds = grpc.metadata_call_credentials(metadata_callback)
        combined_creds = grpc.composite_channel_credentials(cert_creds, auth_creds)

        channel = grpc.secure_channel(
            f"{self.host}:{self.port}",
            combined_creds,
            # options=[
            #     ("grpc.max_send_message_length", kwargs["max_message_length"]),
            #     ("grpc.max_receive_message_length", kwargs["max_message_length"]),
            # ],
        )

        self.lightning_stub = lnrpc.LightningStub(channel)




