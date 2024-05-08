# Author: Éloi Dallaire
# ID: 260794674

import datetime
import doctest

# Global Variables
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Room:
    """
    Represents a room

    Instance attributes: room_type (str), room_num (int), price (float), availability (dict)
    Class attribute: TYPES_OF_ROOMS_AVAILABLE
    """
    # Class attribute
    TYPES_OF_ROOMS_AVAILABLE = ['twin', 'double', 'queen', 'king']  
    
    # Constructor
    def __init__(self, room_type, room_num, price, availability = None):
        self.room_type = room_type
        self.room_num = room_num
        self.price = price
        if availability == None:
            self.availability = {}
        else:
            self.availability = availability
        # Input Validation
        if (type(self.room_type), type(self.room_num), type(self.price), type(self.availability)) != (str, int, float, dict):
            raise AssertionError("at least one of the inputs does not match the expected type")
        if self.room_type.lower() not in Room.TYPES_OF_ROOMS_AVAILABLE:
            raise AssertionError("the room type does not match the available types")
        if self.room_num <= 0:
            raise AssertionError("the room number must be positive")
        if self.price < 0:
            raise AssertionError("the price must be non-negative")
     
     
    def __str__(self):
        """(Room) -> str

        >>> r = Room('King', 132, 129.99)
        >>> r.__str__()
        'Room 132,King,129.99'
        """
        return "Room " + str(self.room_num) + ',' + self.room_type + ',' + str(self.price)


    def set_up_room_availability(self, months, year):
        """(list, int) -> dict

        This will update the availability attribute of the room.
        It takes as input a list of strings representing months and an integer representing the year.
        It returns a dictionary mapping a tuple representing each month of the list to a list of booleans.
        
        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> len(r.availability)
        2
        >>> len(r.availability[(2021, 6)])
        31
        >>> r.availability[(2021, 5)][5]
        True
        >>> print(r.availability[(2021, 5)][0])
        None
        
        >>> r1 = Room("Twin", 132, 59.99)
        >>> r1.set_up_room_availability(['Feb', 'Mar', 'Apr'], 2016)
        >>> len(r1.availability)
        3
        >>> len(r1.availability[(2016, 2)])
        30
        """
        # To account for leap years
        DAYS_PER_MONTH_copy = DAYS_PER_MONTH[:]
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    DAYS_PER_MONTH_copy[1] = 29
            else:
                DAYS_PER_MONTH_copy[1] = 29

        
        for month in months:
            # To find the number of days for the corresponding month
            i = MONTHS.index(month)
            num_days = DAYS_PER_MONTH_copy[i]
            # To create the list of booleans
            bool_list = [None]
            for days in range(num_days):
                bool_list.append(True)
            # To update the dictionary
            self.availability[(year, i+1)] = bool_list            
           
       
    def reserve_room(self, date):
        """(Date) -> Nonetype

        It takes as input an object of type date.
        This will update the availability of the specified room. 

        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.reserve_room(date1)
        >>> r.availability[(2021, 6)][20]
        False

        >>> r1 = Room("Twin", 132, 59.99)
        >>> r1.set_up_room_availability(['Feb', 'Mar', 'Apr'], 2016)
        >>> date2 = datetime.date(2016, 3, 15)
        >>> r1.reserve_room(date2)
        >>> r1.availability[(2016, 3)][15]
        False
        
        r1 = Room("Twin", 132, 59.99)
        r1.set_up_room_availability(['Feb', 'Mar', 'Apr'], 2016)
        r1.availability[(2016, 3)][15] = False
        date2 = datetime.date(2016, 3, 15)
        r1.reserve_room(date2)
        Traceback (most recent call last):
        AssertionError: the room is not available at the given date
        """
        if self.availability[(date.year, date.month)][date.day]:
            self.availability[(date.year, date.month)][date.day] = False
        else:
            raise AssertionError("the room is not available at the given date")
        

    def make_available(self, date):
        """ (Date) -> NoneType

        It takes as input an object of type date.
        This update the availability of a specific room at a given date to be True.

        >>> r = Room("Queen", 105, 80.0)
        >>> r.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 6, 20)
        >>> r.make_available(date1)
        >>> r.availability[(2021, 6)][20]
        True

        >>> r1 = Room("Twin", 132, 59.99)
        >>> r1.set_up_room_availability(['Feb', 'Mar', 'Apr'], 2016)
        >>> date2 = datetime.date(2016, 3, 15)
        >>> r1.availability[(2016, 3)][15] = False
        >>> r1.make_available(date2)
        >>> r1.availability[(2016, 3)][15]
        True
        """
        self.availability[(date.year, date.month)][date.day] = True
      
      
    def is_available(self, check_in, check_out):
        """ (Date, Date) -> bool

        It takes as input two object of type date.
        It returns True if the room is available for the whole
        duration covered between the check-in and check-out date. 

        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> date1 = datetime.date(2021, 5, 25)
        >>> date2 = datetime.date(2021, 6, 10)
        >>> r1.is_available(date1, date2)
        True
        >>> r1.availability[(2021, 5)][28] = False
        >>> r1.is_available(date1, date2)
        False
        
        >>> r2 = Room("Twin", 132, 59.99)
        >>> r2.set_up_room_availability(['Feb', 'Mar', 'Apr'], 2020)
        >>> date1 = datetime.date(2020, 2, 25)
        >>> date2 = datetime.date(2020, 6, 2)
        >>> r2.is_available(date1, date2)
        False
        
        >>> r2 = Room("Twin", 132, 59.99)
        >>> r2.set_up_room_availability(['Feb', 'Mar', 'Apr'], 2020)
        >>> date1 = datetime.date(2020, 4, 25)
        >>> date2 = datetime.date(2020, 2, 2)
        >>> r2.is_available(date1, date2)
        Traceback (most recent call last):
        AssertionError: the check-in date must be earlier than the check-out date
        """
        # Input Validation
        if check_out <= check_in:
            raise AssertionError("the check-in date must be earlier than the check-out date")
        
        stay_len = check_out - check_in
        current_date = check_in
        for i in range(stay_len.days):
            try:
                if not self.availability[(current_date.year, current_date.month)][current_date.day]:
                    return False
                else:
                    current_date += datetime.timedelta(1)
            # If at least one month covered by the stay is not part of the keys of the availability dictionary
            except KeyError:
                return False
        # If the room is available for the whole duration of the stay
        return True
    
    
    @staticmethod 
    def find_available_room(room_list, room_type, check_in, check_out):
        """ (list, str, Date, Date) -> Room

        It takes as input a list of object of type Room, a string corresponding
        to a room type and two dates, the check_in and the check_out date.
        It returns the first available room from the list with the correct room type. 

        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> r2.set_up_room_availability(['May'], 2021)
        >>> r3.set_up_room_availability(['May'], 2021)
        >>> r1.availability[(2021, 5)][8] = False
        >>> r = [r1, r2, r3]
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
        >>> my_room == r3
        True

        >>> r1 = Room("Twin", 132, 68.0)
        >>> r2 = Room("Queen", 133, 65.0)
        >>> r1.set_up_room_availability(['Mar'], 2019)
        >>> r2.set_up_room_availability(['Mar'], 2019)
        >>> r1.set_up_room_availability(['Apr'], 2019)
        >>> r2.set_up_room_availability(['Apr'], 2019)
        >>> r1.availability[(2019, 3)][14] = False
        >>> r1.availability[(2019, 3)][15] = False
        >>> r = [r1, r2]
        >>> date1 = datetime.date(2019, 3, 10)
        >>> date2 = datetime.date(2019, 4, 10)
        >>> my_room = Room.find_available_room(r, 'Twin', date1, date2)
        >>> my_room == None
        True
        """
        for room in room_list:
            # To check the availability of the room
            if room.is_available(check_in, check_out):
                # To check if the room type is appropriate
                if room.room_type == room_type:
                    return room
        # If no room are available        
        return None
        

if __name__ == '__main__':
    doctest.testmod()
