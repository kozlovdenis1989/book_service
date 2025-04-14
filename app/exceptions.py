class TableNotFound(Exception):
    def __init__(self, message="Table not found"):
        super().__init__(message)
        self.message = message

class TableAlreadyExists(Exception):
    def __init__(self, message="A table with this name or location already exists"):
        super().__init__(message)
        self.message = message

class TimeSlotTaken(Exception):
    def __init__(self, message="Time slot is already taken"):
        super().__init__(message)
        self.message = message

class ReservationNotFound(Exception):
    def __init__(self, message="Reservation not found"):
        super().__init__(message)
        self.message = message