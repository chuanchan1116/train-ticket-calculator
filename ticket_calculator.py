"""TicketCalculator is used for querying ticket price with giver TrainType, 
TicketType, FareClass and CabinClass"""
from rail_api_enum import TrainType, TicketType, FareClass, CabinClass
from rail_api import RailApi


class TicketCalculator:
    def __init__(
        self,
        train_type: TrainType,
        ticket_type: TicketType,
        fare_class: FareClass,
        cabin_class: CabinClass,
        client_id: str,
        client_secret: str,
    ) -> None:
        self._train_type = train_type
        self._ticket_type = ticket_type
        self._fare_class = fare_class
        self._cabin_class = cabin_class
        self._api = RailApi(client_id, client_secret)
        self._stations = self._api.get_stations()

    def price(self, sta1: str, sta2: str) -> int | None:
        fares = self._api.get_fares_by_type(
            self._stations[sta1], self._stations[sta2], self._train_type
        )
        min_ = 999999
        for f in fares:
            if (
                f.ticket_type == self._ticket_type
                and f.fare_class == self._fare_class
                and f.cabin_class == self._cabin_class
            ):
                min_ = min(min_, f.price)
        return min_
