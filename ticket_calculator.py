"""TicketCalculator is used for querying ticket price with giver TrainType, 
TicketType, FareClass and CabinClass"""
from rail_api_enum import TrainType, TicketType, FareClass, CabinClass
from rail_api import TrainStation, RailApi


class TicketCalculator:
    def __init__(
        self,
        train_type: TrainType,
        ticket_type: TicketType,
        fare_class: FareClass,
        cabin_class: CabinClass,
    ) -> None:
        self._train_type = train_type
        self._ticket_type = ticket_type
        self._fare_class = fare_class
        self._cabin_class = cabin_class
        self._api = RailApi()
        self._stations = self._api.get_stations()

    def price(self, sta1: str, sta2: str) -> int | None:
        fares = self._api.get_fares_by_type(
            self._stations[sta1], self._stations[sta2], self._train_type
        )
        for f in fares:
            if (
                f["TicketType"] == self._ticket_type
                and f["FareClass"] == self._fare_class
                and f["CabinClass"] == self._cabin_class
            ):
                return f["Price"]
