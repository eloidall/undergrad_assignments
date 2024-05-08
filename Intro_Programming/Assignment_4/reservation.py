# Author: Éloi Dallaire
# ID: 260794674

import datetime
import doctest
from room import Room, MONTHS, DAYS_PER_MONTH
import random


class Reservation:
    """
    Represents a reservation

    Instance attributes: name (str), room_reserved (Room), check_in (Date), check_out (Date), booking_number (int)
    Class attribute: booking_numbers
    """
    # Class attribute
    booking_numbers = []
    
    # Constructor
    def __init__(self, name, room_reserved, check_in, check_out, booking_number = None):
        """        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-10
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][9]
        False
        """    
        self.name = name
        self.room_reserved = room_reserved
        self.check_in = check_in
        self.check_out = check_out
        
        # To initialize the booking number
        if booking_number == None:
            # To ensure all booking_numbers are different
            self.booking_number = random.randint(1000000000000, 9999999999999)
            while self.booking_number in Reservation.booking_numbers:
                self.booking_number = random.randint(1000000000000, 9999999999999)
        else:
            self.booking_number = booking_number
        
        if self.booking_number in Reservation.booking_numbers:
            raise AssertionError("this booking number is already being used")
            
        # booking_number Validation
        if type(self.booking_number) != int:
            raise AssertionError("the booking number must be of type int")
        if len(str(self.booking_number)) != 13:
            raise AssertionError("the booking number is not a 13 digit number")
        if not self.room_reserved.is_available(self.check_in, self.check_out):
            raise AssertionError("the room is not available at the given dates") 
        
        # To add the appropriate booking_number to the list
        Reservation.booking_numbers.append(self.booking_number)
        
        # To reserve the room for the whole stay
        stay_len = check_out - check_in
        current_date = check_in
        for i in range(stay_len.days):
            self.room_reserved.reserve_room(current_date)
            current_date += datetime.timedelta(1)
            

    def __str__(self):
        """
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> print(my_reservation)
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        return ("Booking number: " + str(self.booking_number) + "\n" + "Name: " + self.name + "\n" + "Room reserved: " + self.room_reserved.__str__() + "\n" + "Check-in date: " + str(self.check_in) + "\n" + "Check-out date: " + str(self.check_out))
      
    
    def to_short_string(self):
        """ (Reservation) -> str
        
        Takes no input and returns a string containing the booking number and name on the reservation
        
        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
        >>> my_reservation.to_short_string()
        '1953400675629--Mrs. Santos'
        """
        return str(self.booking_number) + "--" + self.name
    
        
    @classmethod
    def from_short_string(cls, short_string, check_in, check_out, room_reserved):
        """ (str, Date, Date, Room) -> Reservation

        Takes as input a string in the format return by the to_short_string
        function, a check_in and check_out date, and an object of type Room.
        It returns an object of type Reservation for a stay in the specified room. 
        
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 4)
        >>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos', date1, date2, r1)
        >>> print(my_reservation.check_in)
        2021-05-03
        >>> print(my_reservation.check_out)
        2021-05-04
        >>> my_reservation.booking_number
        1953400675629
        >>> r1.availability[(2021, 5)][3]
        False
        """
        reservation_element = short_string.split('--')
        return cls(reservation_element[1], room_reserved, check_in, check_out, int(reservation_element[0]))
        
        
    @staticmethod
    def get_reservations_from_row(room_reserved, rsv_strs):
        """ (Room, tuple) -> dict
        
        It takes as input an object of type Room and a list of tuple in the same
        format as the function Hotel.load_reservation_strings_for_month.
        It returns a dictionary mapping the reservation number to the Reservation object.

        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(MONTHS, 2021)
        >>> rsv_strs = [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 4, '1953400675629--Jack')]
        >>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
        >>> print(rsv_dict[1953400675629])
        Booking number: 1953400675629
        Name: Jack
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-05
        """
        # To create a temporary dictionary mapping all the dates to the same reservation short_string
        temp_dict = {}
        for element in rsv_strs:
            # To add to the dictionary
            if len(element[3]) > 1:
                # Adequate date
                date = datetime.date(element[0], MONTHS.index(element[1])+1, element[2])
                if element[3] not in temp_dict:
                    temp_dict[element[3]] = [date]
                else:
                    temp_dict[element[3]].append(date)
                
        # To create the dictionary output                
        rsv_dict = {}
        for k, v in temp_dict.items():
            booking_number = int(k.split('--')[0])
            rsv_dict[booking_number] = Reservation.from_short_string(k, min(v), max(v)+datetime.timedelta(1), room_reserved)
            
        return rsv_dict           
            
  
if __name__ == '__main__':
    doctest.testmod()
    
    
            