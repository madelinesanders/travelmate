from abc import ABC, abstractmethod

class TripSortStrategy(ABC):
    @abstractmethod
    def sort(self, trips):
        pass

class SortByStartDateStrategy(TripSortStrategy):
    def sort(self, trips):
        return trips.order_by('start_date')

class SortByEndDateStrategy(TripSortStrategy):
    def sort(self, trips):
        return trips.order_by('end_date')

class SortByLocationStrategy(TripSortStrategy):
    def sort(self, trips):
        return trips.order_by('location')

class SortByDurationStrategy(TripSortStrategy):
    def sort(self, trips):
        trips_with_duration = [(trip, (trip.end_date - trip.start_date).days) for trip in trips]
        trips_with_duration.sort(key=lambda x: x[1])
        return [trip for trip, _ in trips_with_duration]

class TripSorter:
    def __init__(self, strategy: TripSortStrategy):
        self.strategy = strategy

    def sort_trips(self, trips):
        return self.strategy.sort(trips)