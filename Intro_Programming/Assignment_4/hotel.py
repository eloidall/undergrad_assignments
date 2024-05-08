# Author: Éloi Dallaire
# ID: 260794674

import doctest
import datetime
import random
import copy
import os
from room import Room, MONTHS, DAYS_PER_MONTH
from reservation import Reservation


class Hotel:
    """
    Represents an hotel's reservations

    Instance attributes: name (str), rooms (list), reservations (dict)
    """    
    # Constructor
    def __init__(self, name, rooms = None, reservations = None):
        # To copy the last two inputs
        rooms_copy = copy.deepcopy(rooms)
        reservations_copy = copy.deepcopy(reservations)
        # To initialize the attributes
        self.name = name
        if rooms_copy == None:
            self.rooms = []
        else:
            self.rooms = rooms_copy
        if reservations_copy == None:
            self.reservations = {}
        else:
            self.reservations = reservations_copy
    
    
    def make_reservation(self, client_name, room_type, check_in, check_out):
        """ (str, str, Date, Date) -> int

        Returns the booking number of the reservation created
        with the first available room of the specified type.

        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        1953400675629
        >>> print(h.reservations[1953400675629])
        Booking number: 1953400675629
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        # To check if a room is available
        available_room = Room.find_available_room(self.rooms, room_type, check_in, check_out)
        if available_room == None:
            raise AssertionError("no room of the given type is available for the dates indicated")
        else:
            # To make the reservation and update the dictionary
            client_reservation = Reservation(client_name, available_room, check_in, check_out)
            self.reservations[client_reservation.booking_number] = client_reservation
            
        return client_reservation.booking_number
    
        
    def get_receipt(self, rsv_list):
        """ (list) -> float

        Takes as input a list of integer representing booking number.
        It returns the total amount that the client must pay to the hotel.

        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.get_receipt([num1])
        560.0
        >>> date3 = datetime.date(2021, 6, 5)
        >>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
        >>> h.get_receipt([num1, num2])
        2375.0
        >>> h.get_receipt([123])
        0.0
        """
        total_amount = 0
        for booking_number in rsv_list:
            # To skip if the reservation is not from this hotel
            if booking_number not in self.reservations:
                total_amount += 0.0
            # To add the total value of the stay to the amount
            else:
                # To compute number of days
                reservation = self.reservations[booking_number]
                stay_len = reservation.check_out - reservation.check_in
                # To compute total amount
                room_reserved = reservation.room_reserved
                price = room_reserved.price
                total_amount +=  stay_len.days * price
        return total_amount
        
    
    def get_reservation_for_booking_number(self, booking_number):
        """ (int) -> Reservation

        Takes as input a booking number and return the Reservation object.

        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> rsv = h.get_reservation_for_booking_number(num1)
        >>> print(rsv)
        Booking number: 4191471513010
        Name: Mrs. Santos
        Room reserved: Room 105,Queen,80.0
        Check-in date: 2021-05-03
        Check-out date: 2021-05-10
        """
        if (type(booking_number), len(str(booking_number)))!= (int, 13):
               raise AssertionError("the booking number must be a 13 digit integer")
        if booking_number not in self.reservations:
            return None
        else:
            return self.reservations[booking_number]

    
    def cancel_reservation(self, booking_number):
        """ (int) -> NoneType

        Takes as input a booking number.
        Cancels the reservation and make available the room. 

        >>> r1 = Room("Queen", 105, 80.0)
        >>> r1.set_up_room_availability(['May'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1])
        >>> date1 = datetime.date(2021, 5, 3)
        >>> date2 = datetime.date(2021, 5, 10)
        >>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
        >>> h.cancel_reservation(num1)
        >>> num1 in h.reservations
        False
        >>> r1.availability[(2021, 5)][4]
        True
        """
        # If reservation not found
        if booking_number not in self.reservations:
            return
        else:
            # To access the Reservation object and attributes
            reservation = self.reservations[booking_number]
            check_in = reservation.check_in
            check_out = reservation.check_out
            # To access the Room object
            room_reserved = reservation.room_reserved
            
            # To make available all days of the stay
            stay_len = check_out - check_in
            current_date = check_in
            for i in range(stay_len.days):
                room_reserved.make_available(current_date)
                current_date += datetime.timedelta(1)
            
            # To remove from the dictionary
            self.reservations.pop(booking_number)
        
     
    def get_available_room_types(self):
        """ (Hotel) -> list

        Takes no input and returns a list of all available room types at the hotel.

        >>> r1 = Room("Queen", 105, 80.0)
        >>> r2 = Room("Twin", 101, 55.0)
        >>> r3 = Room("Queen", 107, 80.0)
        >>> r1.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r2.set_up_room_availability(['May', 'Jun'], 2021)
        >>> r3.set_up_room_availability(['May', 'Jun'], 2021)
        >>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
        >>> types = h.get_available_room_types()
        >>> types.sort()
        >>> types
        ['Queen', 'Twin']
        """
        available_types = []
        for room in self.rooms:
            if room.room_type not in available_types:
                available_types.append(room.room_type)
        return available_types


    @staticmethod
    def load_hotel_info_file(file_path):
        """ (str) -> tuple

        Takes as input a file path and returns a tuple with
        the name of the hotel and a list of the Rooms object.

        >>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> hotel_name
        'Overlook Hotel'
        >>> print(len(rooms))
        500
        >>> print(rooms[236])
        Room 237,Twin,99.99
        """
        # To add each line into a list
        fobj = open(file_path, 'r')
        string_list = []
        for line in fobj:
            new_line = line.strip('\n')
            string_list.append(new_line)
        fobj.close()
   
        # To separate the hotel name and the rooms
        hotel_name = string_list[:1]
        hotel_name = hotel_name[0]
        rooms_str = string_list[1:]
        
        # To create the Room objects
        rooms_list = []
        for x in rooms_str:
            elements = x.split(',')
            # To get all the attributes
            room_num = int(elements[0].strip('Room '))
            room_type = elements[1]
            room_price = float(elements[2])
            # To add the Room object
            rooms_list.append(Room(room_type, room_num, room_price))
        
        # To return the tuple
        return (hotel_name, rooms_list)
        
        
    def save_hotel_info_file(self):     
        """ (Hotel) -> NoneType

        Takes no explicit input.
        Save the hotel info into a new file in the appropriate directory.

        >>> r1 = Room("Double", 101, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> h.save_hotel_info_file()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 101,Double,99.99\\n'
        >>> fobj.close()
        """
        # To create the proper file and path names        
        file_name = "hotel_info.txt"
        
        file_path = self.name.lower()
        file_path = "hotels/" + file_path.replace(' ', '_') + "/"
        
        complete_name = file_path + file_name
        
        # To write the hotel name and the rooms list        
        fobj = open(complete_name, 'w', encoding ='utf-8')       
        fobj.write(self.name + '\n')
        for room in self.rooms:
            fobj.write(room.__str__() + '\n')    
        fobj.close()


    @staticmethod
    def load_reservation_strings_for_month(folder_name, month, year):
        """ (str, str, int) -> dict

        Takes as input a folder name, a month and a year.
        Returns a dictionary mapping each room number to a list of tuple
        corresponding to the reservation data for that room for that month.

        >>> name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
        >>> h = Hotel(name, rooms, {})
        >>> rsvs = h.load_reservation_strings_for_month('overlook_hotel', 'Oct', 1975)
        >>> print(rsvs[237])
        [(1975, 'Oct', 1, ''), (1975, 'Oct', 2, ''), (1975, 'Oct', 3, ''), (1975, 'Oct', 4, ''), (1975, 'Oct', 5, ''), (1975, 'Oct', 6, ''), (1975, 'Oct', 7, ''), (1975, 'Oct', 8, ''), (1975, 'Oct', 9, ''), (1975, 'Oct', 10, ''), (1975, 'Oct', 11, ''), (1975, 'Oct', 12, ''), (1975, 'Oct', 13, ''), (1975, 'Oct', 14, ''), (1975, 'Oct', 15, ''), (1975, 'Oct', 16, ''), (1975, 'Oct', 17, ''), (1975, 'Oct', 18, ''), (1975, 'Oct', 19, ''), (1975, 'Oct', 20, ''), (1975, 'Oct', 21, ''), (1975, 'Oct', 22, ''), (1975, 'Oct', 23, ''), (1975, 'Oct', 24, ''), (1975, 'Oct', 25, ''), (1975, 'Oct', 26, ''), (1975, 'Oct', 27, ''), (1975, 'Oct', 28, ''), (1975, 'Oct', 29, ''), (1975, 'Oct', 30, '9998701091820--Jack'), (1975, 'Oct', 31, '9998701091820--Jack')]
        """
        # To create the complete file name
        complete_file_name = "hotels/" + folder_name + "/" + str(year) + "_" + month + ".csv"

        # To return a nested list of the elements in the CSV file
        matrix = []
        fobj = open(complete_file_name, 'r', encoding ='utf-8')
        for line in fobj:
            new_line = line.strip()
            matrix.append(new_line.split(","))
        fobj.close()
        
        # To create the output dictionary
        rsvs_dict = {}    
        for i in matrix:
            for j, v in enumerate(i):
                if int(i[0]) not in rsvs_dict:
                    rsvs_dict[int(i[0])] = [(year, month, j, i[j])]
                else:
                    rsvs_dict[int(i[0])].append((year, month, j, i[j]))
                    
        # To remove the element with date 0
        for room in rsvs_dict.values():
           room.remove(room[0])

        return rsvs_dict      
                

    def save_reservations_for_month(self, month, year):
        """ (str, int) -> NoneType

        Takes as input a month and a year.
        Creates a CSV file with all the reservation info for that month. 

        >>> random.seed(987)
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> Reservation.booking_numbers = []
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> num = h.make_reservation("Jack", "Double", date1, date2)
        >>> h.save_reservations_for_month('Oct', 2021)
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        # To create proper names
        file_path = self.name.lower()
        file_path = 'hotels/' + file_path.replace(' ', '_') + '/'
        
        complete_name = file_path + str(year) + '_' + month + '.csv'
        
        # To find the number of columns for the month, accounting for leap years
        DAYS_PER_MONTH_copy = DAYS_PER_MONTH[:]
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    DAYS_PER_MONTH_copy[1] = 29
            else:
                DAYS_PER_MONTH_copy[1] = 29
                
        month_index = MONTHS.index(month)
        num_days = DAYS_PER_MONTH_copy[month_index]
        
        # To create a matrix with all the info to write in the .csv file
        matrix = []
        for room in self.rooms:
            # To create a virgin sub-list for each room
            room_rsv = []
            room_rsv.append(room.room_num)
            for i in range(num_days):
                room_rsv.append('')
            matrix.append(room_rsv)

        # To add the reservations to the appropriate sub-list
        for rsv in self.reservations.values():
            # To access the proper attributes and object
            short_string = rsv.to_short_string()
            room_reserved = rsv.room_reserved
            room_number = room_reserved.room_num
            
            # To find proper range even if reservation is spread on several months
            start_range = max(rsv.check_in, datetime.date(year, month_index+1, 1))
            end_range = min(rsv.check_out, datetime.date(year, month_index+1, num_days))
            month_range = end_range - start_range
            
            # To add the short string at the right position
            current_date = start_range
            for date in range(month_range.days+1):
                for r in matrix:
                    if r[0] == room_number:
                        r[current_date.day] = short_string
                        current_date += datetime.timedelta(1)               
        matrix.sort()
        
        # To write in the .csv file
        fobj = open(complete_name, 'w', encoding ='utf-8')
        for row in matrix:
            for i, x in enumerate(row):
                to_append = str(x)
                if i < len(row)-1:
                    to_append += ','
                fobj.write(to_append)
                to_append = ''
            fobj.write('\n')
        fobj.close()
        
            
    def save_hotel(self):
        """
        (Hotel) -> NoneType

        Takes no explicit input and saves the hotel_info.txt
        file and all the CSV files containing the reservations info. 

        >>> random.seed(987)
        >>> Reservation.booking_numbers = []
        >>> r1 = Room("Double", 237, 99.99)
        >>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
        >>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
        >>> date1 = datetime.date(2021, 10, 30)
        >>> date2 = datetime.date(2021, 12, 23)
        >>> h.make_reservation("Jack", "Double", date1, date2)
        1953400675629
        >>> h.save_hotel()
        >>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
        >>> fobj.read()
        'Queen Elizabeth Hotel\\nRoom 237,Double,99.99\\n'
        >>> fobj.close()
        >>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
        >>> fobj.read()
        '237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
        >>> fobj.close()
        """
        # To retrieve the months of availability for the hotel
        months_available = []
        
        # To add all months there's a reservation
        for rsv in self.reservations.values():
            current_year = rsv.check_in.year
            check_in_month = rsv.check_in.month
            check_out_month = rsv.check_out.month
            for i in range(check_in_month, check_out_month+1):
                months_available.append(MONTHS[i-1])
        
        # To check every months
        for month in range(1,13):
            # To check every room for the same day of the month
            current_day= 1
            current_date = datetime.date(current_year, month, current_day)
            for room in self.rooms:
                # To add the month if available
                if room.is_available(current_date, current_date +datetime.timedelta(1)):
                    if MONTHS[month-1] not in months_available:
                        months_available.append(MONTHS[month-1])
                    break
            # If all rooms are unavailable for that day, verify the next day
            current_day += 1
        
        # To retrieve the names
        file_path = self.name.lower()
        file_path = 'hotels/' + file_path.replace(' ', '_') + '/' 
        # To create the folder if inexistant
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            
        # To create the hotel_info.txt file
        self.save_hotel_info_file()
        # To create the .csv files
        for m in months_available:
            self.save_reservations_for_month(m, current_year)
         
    
    @classmethod
    def load_hotel(cls, folder_name):
        """ (type, str) -> Hotel

        Takes as input a folder name.
        Loads the hotel info file and the CSV files from inside that folder. 
        Returns an object of type Hotel with loaded name, rooms and reservations info. 

        >>> random.seed(137)
        >>> Reservation.booking_numbers = []
        >>> hotel = Hotel.load_hotel('overlook_hotel')
        >>> hotel.name
        'Overlook Hotel'
        >>> str(hotel.rooms[236])
        'Room 237,Twin,99.99'
        >>> print(hotel.reservations[9998701091820])
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        """
        complete_folder_name = 'hotels/' + folder_name
        file_list = os.listdir(complete_folder_name)
        
        # To load the hotel_info.txt file
        for file in file_list:
            if file[-14:] == 'hotel_info.txt':
                (hotel_name, rooms) = Hotel.load_hotel_info_file(complete_folder_name + '/' + file)
                file_list.remove('hotel_info.txt')
                
        # To create the Hotel object
        h = Hotel(hotel_name, rooms)
        
        rsvs_dict_list = {}
        for file in file_list:
            # To load .csv files info
            temp_rsvs_dict = h.load_reservation_strings_for_month(folder_name, file[-7:-4], int(file[-12:-8]))
            # To update availability for the month loaded
            for room in h.rooms:
                room.set_up_room_availability([file[-7:-4]], int(file[-12:-8]))
            # To merge all months in one dictionary
            for k, v in temp_rsvs_dict.items():
                if k not in rsvs_dict_list:
                    rsvs_dict_list[k] = v
                else:
                    rsvs_dict_list[k] += v
        # To create the proper reservations
        for room_num, dates_list in rsvs_dict_list.items():
            rsvs_dict = Reservation.get_reservations_from_row(h.rooms[room_num-1], dates_list)
            for booking_number, rsv in rsvs_dict.items():
                h.reservations[booking_number] = rsv
        # To return the updated hotel object       
        return h
             

if __name__ == '__main__':
    doctest.testmod()

