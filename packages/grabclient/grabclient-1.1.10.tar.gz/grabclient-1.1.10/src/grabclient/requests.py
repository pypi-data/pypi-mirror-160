from typing import List

from grabclient.common import Origin, Package, Destination, \
    ServiceType, CashOnDelivery, Sender, Recipient, PaymentMethod


class DeliveryQuoteRequest:
    __slots__ = (
        'service_type', 'packages', 'origin', 'destination'
    )

    def __init__(self,
                 packages: List[Package],
                 origin: Origin,
                 destination: Destination,
                 service_type: ServiceType):
        self.service_type = service_type
        self.origin = origin
        self.destination = destination
        self.packages = packages


class DeliveryRequest:
    __slots__ = (
        'merchant_order_id',
        'service_type',
        'packages',
        'payment_method',
        'sender',
        'recipient',
        'origin',
        'destination'
    )

    def __init__(self,
                 merchant_order_id: str,
                 service_type: ServiceType,
                 packages: List[Package],
                 payment_method: PaymentMethod,
                 sender: Sender,
                 recipient: Recipient,
                 origin: Origin,
                 destination: Destination):
        self.merchant_order_id = merchant_order_id
        self.service_type = service_type
        self.packages = packages
        self.payment_method = payment_method
        self.sender = sender
        self.recipient = recipient
        self.origin = origin
        self.destination = destination
