class DeskNotFound(Exception):
    def __init__(self, message="Desk not found"):
        super().__init__(message)
        self.message = message

class DeskAlreadyExists(Exception):
    def __init__(self, message="A desk with this name or location already exists"):
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