# Author: Éloi Dallaire
# ID: 260794674


import doctest
import datetime
import random
import matplotlib.pyplot as plt
import os
from hotel import Hotel
from reservation import Reservation


def helper_reformat_date(date_str):
    """ (str) -> Date

    Takes as input a date string in format YYYY-MM-DD.
    Returns the date in the datetime.date format.
    """
    date_str = date_str.split('-')
    for e in date_str[1:3]:
        if e[0] == '0':
            e = e[1:]
    # To convert to proper format
    date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
    return date 


class Booking:
       
    # Constructor
    def __init__(self, hotel_list):
        """ (type) -> Booking

        Takes no explicit input.
        Loads all hotels in the hotels/ folder and creates
        an object of type Booking with the list of all hotels.
        
        >>> Reservation.booking_numbers = []
        >>> system = Booking.load_system()
        >>> len(system.hotels)
        2
        >>> system.hotels[1].name
        'The Great Northern Hotel'
        >>> print(system.hotels[1].rooms[314])
        Room 315,Queen,129.99
        """        
        if type(hotel_list) != list:
            raise AssertionError("the input must be a list")
        self.hotels = hotel_list
        
                
    @classmethod
    def load_system(cls):

        file_list = os.listdir('hotels/')
        
        # To create a list with all Hotel object from the folder
        hotels_list = []
        for hotel_folder in file_list:
            h = Hotel.load_hotel(hotel_folder)
            hotels_list.append(h)
        return cls(hotels_list)
         
        
    def menu(self):
        """ (Booking) -> NoneType

        Takes no explicit input.
        Display to the user the menu.
        
        >>> Reservation.booking_numbers = []    
        >>> booking = Booking.load_system()
        >>> booking.menu()
        Welcome to Booking System
        What would you like to do?
        1     Make a reservation
        2     Cancel a reservation
        3     Look up a reservation
        > 1
        """
        user_operations = input("Welcome to Booking System" + '\n' + "What would you like to do?" + '\n' + "1     Make a reservation" +
                                '\n' + "2     Cancel a reservation" + '\n' + "3     Look up a reservation" + '\n> ')
        # To call the appropriate method
        if user_operations == 'xyzzy':
            self.delete_reservations_at_random()
        if user_operations == '1':
            self.create_reservation()
        if user_operations == '2':
            self.cancel_reservation()
        if user_operations == '3':
            self.lookup_reservation()
        else:
            print("Please enter a valid option")
            
        # To save back to disk
        for h in self.hotels:
            h.save_hotel()        

       
    def create_reservation(self):
        """ (Booking) -> NoneType

        Takes no explicit input.
        Prompt the user to enter reservation
        info and proceed to the reservation.
        
        >>> Reservation.booking_numbers = []
        >>> random.seed(137)
        >>> booking = Booking.load_system()
        >>> booking.create_reservation()
        Please enter your name: Judy
        Hi Judy! Which hotel would you like to book?
        1 The Great Northern Hotel
        2 Overlook Hotel
        > 1
        Which type of room would you like?
        1 Double
        2 Twin
        3 King
        4 Queen
        Page 16> 1
        Enter check-in date (YYYY-MM-DD): 1989-01-01
        Enter check-out date (YYYY-MM-DD): 1989-01-04
        Ok. Making your reservation for a Double room.
        Your reservation number is: 4191471513010
        Your total amount due is: $459.84.
        Thank you!
        """
        # To get the user name
        client_name = input("Please enter your name: ")
        
        # To form the list of hotels in a string
        list_hotel_str = ''
        i = 1
        for h in self.hotels:
            hotel_str = str(i) + "     " + h.name + '\n'
            list_hotel_str += hotel_str
            i += 1
        # To get the user choice of hotel
        try:
            hotel_input = input("Hi " + client_name + "! Which hotel would you like to book?\n" + list_hotel_str + "> ")
            hotel_choice = self.hotels[int(hotel_input)-1]
        except IndexError:
            print("Please enter a valid option.")
            return
        
        # To get all the available room types and to display them in a string
        room_types = hotel_choice.get_available_room_types()
        room_types_str = ''
        j = 1
        for r in room_types:
            room_type_str = str(j) + "     " + r + '\n'
            room_types_str += room_type_str
            j += 1
        
        # To get the user room type
        try:
            room_input = input("Which type of room would you like?\n" + room_types_str + "> ")
            room_choice = room_types[int(room_input)-1]
        except IndexError:
            print("Please enter a valid option.")
            return
        
        # To get the check-in and check-out dates
        check_in = helper_reformat_date(input("Enter check-in date (YYYY-MM-DD): "))
        check_out = helper_reformat_date(input("Enter check-out date (YYYY-MM-DD): "))

        # To make the reservation
        try:
            rsv_booking_number = hotel_choice.make_reservation(client_name, room_choice, check_in, check_out)
            amount_due = hotel_choice.get_receipt([rsv_booking_number])
        except AssertionError:
            print("No room of the given type is available for the dates indicated in this hotel")
            return
        
        # To display all the reservation info
        print("Ok. Making your reservation for a " + room_choice + " room.\nYour reservation number is: "
              + str(rsv_booking_number) + "\nYour total amount due is: $" + str(round(amount_due,2)) + ".\nThank you!")
        
    
    
    def cancel_reservation(self):
        """ (Booking) -> NoneType

        Takes no explicit input.
        Prompt the user with a reservation number and try to cancel it.
        
        >>> Reservation.booking_numbers = []
        >>> booking = Booking.load_system()
        >>> booking.cancel_reservation()
        Please enter your booking number: 9998701091820
        Cancelled successfully.
        >>> booking.cancel_reservation()
        Please enter your booking number: 9998701091820
        Could not find a reservation with that booking number.
        """
        # User booking number
        booking_number = int(input("Please enter your booking number: "))
        
        member = False
        for h in self.hotels:
            # To cancel the reservation and save the hotel
            if booking_number in h.reservations:
                h.cancel_reservation(booking_number)
                member = True
                print("Cancelled successfully")
        # If reservation not found
        if not member:
            print("Could not find a reservation with that booking number.")
        


    def lookup_reservation(self):
        """ (Booking) -> NoneType

        Takes no explicit input.
        Asks the user for the info related to their reservation(s)
        and displays the whole reservation if found.
        
        >>> Reservation.booking_numbers = []
        >>> booking = Booking.load_system()
        >>> booking.lookup_reservation()
        Do you have your booking number(s)? yes
        Please enter a booking number (or 'end'): 9998701091820
        Please enter a booking number (or 'end'): end
        Reservation found at hotel Overlook Hotel:
        Booking number: 9998701091820
        Name: Jack
        Room reserved: Room 237,Twin,99.99
        Check-in date: 1975-10-30
        Check-out date: 1975-12-24
        Total amount due: $5499.45

        >>> booking.lookup_reservation()
        Do you have your booking number(s)? no
        Please enter your name: Judy
        Please enter the hotel you are booked at: The Great Northern Hotel
        Enter the reserved room number: 315
        Enter the check-in date (YYYY-MM-DD): 1989-01-01
        Enter the check-out date (YYYY-MM-DD): 1989-12-31
        Reservation found under booking number 3020747285952.
        Here are the details:
        Booking number: 3020747285952
        Name: Judy
        Room reserved: Room 315,Queen,129.99
        Check-in date: 1989-01-01
        Check-out date: 1990-01-01
        Total amount due: $47446.35
        """
        user_info = input("Do you have your booking number(s)? ")
        
        # If the user does have the booking number
        if user_info.lower() == 'yes':
            # To get all the of the user's booking number into a list
            booking_numbers_to_lookup = []
            booking_number = input("Please enter a booking number (or 'end'): ")
            
            # To keep asking until the user enters 'end'
            while booking_number.lower() != 'end':
                if int(booking_number) not in booking_numbers_to_lookup:
                    booking_numbers_to_lookup.append(int(booking_number))
                booking_number = input("Please enter a booking number (or 'end'): ")
            
            # To retrieve all the output info
            output_str = ''        
            for x in booking_numbers_to_lookup:
                rsv_str = ''
                # To look in every hotels
                for h in self.hotels:
                    rsv = h.get_reservation_for_booking_number(x)
                    # To check the next hotel
                    if rsv == None:
                        continue
                    # To add all the reservation info to the relative string
                    client_hotel = h
                    total_amount = h.get_receipt([rsv.booking_number])
                    rsv_str += "Reservation found at " + client_hotel.name + ":\n" + rsv.__str__()
                    rsv_str += "\nTotal amount due: $" + str(round(total_amount, 2)) + "\n"
                    break
                # To add the relative string to the final string    
                if rsv_str == '':
                    output_str += "\nNo reservation found with this booking number: " + str(x)
                else:
                    output_str += rsv_str
            # To print the final string
            print(output_str)
            

        # If the user does not have the booking number
        if user_info.lower() == 'no':
            # To get all the user info
            client_name = input("Please enter your name: ")
            client_hotel = input("Please enter the hotel you are booked at: ")
            room_num = int(input("Enter the reserved room number: "))
            check_in = helper_reformat_date(input("Enter the check-in date (YYYY-MM-DD): "))
            check_out = helper_reformat_date(input("Enter the check-out date (YYYY-MM-DD): "))
            
            # To retrive all the output info
            output_str = ''
            for h in self.hotels:
                # To find the right hotel
                if h.name == client_hotel:
                    for rsv in h.reservations.values():
                        # To find the right reservation
                        if (rsv.name, rsv.room_reserved.room_num, rsv.check_in, rsv.check_out) == (client_name, room_num, check_in, check_out):
                            # To add the related info to the output string
                            total_amount = h.get_receipt([rsv.booking_number])
                            output_str += "Reservation found under booking number " + str(rsv.booking_number)
                            output_str += ".\nHere are the details:\n" + rsv.__str__() + '\nTotal amount due: $' + str(round(total_amount, 2))
                            break
            # To print out the output string           
            if output_str == '':
                print("No reservation found with the provided info.")
                return
            print(output_str)
                      
               
    def delete_reservations_at_random(self):
        """ (Booking) -> NoneType

        Takes no explicit input.
        Delete all the reservations of an hotel at random.

        >>> Reservation.booking_numbers = []
        >>> random.seed(1338)
        >>> booking = Booking.load_system()
        >>> booking.delete_reservations_at_random()
        You said the magic word!
        >>> len(booking.hotels[1].reservations)
        0
        >>> len(booking.hotels[0].reservations)
        1
        """
        print("You said the magic word!")
        
        # To choose an hotel at random
        h = self.hotels[random.randint(0, len(self.hotels)-1)]
        
        # To cancel all reservations
        for rsv in list(h.reservations):
            h.cancel_reservation(rsv)
        

    def plot_occupancies(self, month):
        """ (Booking, str) -> tuple

        Plot all the reservations of an hotel on one line. Does that for every hotel.
        Returns a list of tuple with all x-values and y-values for every hotel.

        >>> Reservation.booking_numbers = []
        >>> booking = Booking.load_system()
        >>> booking.plot_occupancies('Oct')
        [([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]), ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])]
        """
        file_list = os.listdir('hotels/')
        plot_info = []
        # To iterate over each hotel
        for hotel_folder in file_list:
            hotel_file_list = os.listdir('hotels/' + hotel_folder)
            
            # To return a matrix with the occurence of required month(s)
            for file in hotel_file_list:
                final_matrix = []
                if file[-7:-4] == month:                    
                    # To transpose the content of the csv file into a matrix
                    matrix = []
                    fobj = open('hotels/' + hotel_folder + '/' + file, 'r', encoding ='utf-8')
                    for line in fobj:
                        new_line = line.strip()
                        matrix.append(new_line.split(","))
                    fobj.close()
                    # To take out the room number
                    for i, room in enumerate(matrix):
                        room = room[1:]
                        matrix[i] = room
                        
                    # To count number of reservations per day
                    num_rows = len(matrix)
                    num_columns = len(matrix[0]) 
                    rsv_occurrence = []
                    for c in range(num_columns):
                        rsv_count = 0
                        for r in range(num_rows):
                            if len(matrix[r][c]) > 1:
                                rsv_count += 1
                        rsv_occurrence.append(rsv_count) 
                    # To cumulate occurrences of the same month over different years
                    if len(final_matrix) > 1:
                        for i, row in enumerate(final_matrix):
                            for j, col in enumerate(row):
                                col += matrix[i][j]
                    else:
                        final_matrix = matrix
                        
            # To add the hotel plot info    
            plot_info.append((hotel_folder,rsv_occurrence))
        
        # To plot the data
        plot_info_copy = []
        x_coord = list(range(len(plot_info[0][1])))
        for i, h in enumerate(plot_info):
            
            # To create the appropriate label
            hotel_name = h[0].replace('_', ' ')
            hotel_name = hotel_name.split()            
            for i, word in enumerate(hotel_name):
                word_copy = ''
                for j, char in enumerate(word):
                    if j == 0:
                        word_copy += char.upper()
                    else:
                        word_copy += char
                hotel_name[i] = word_copy
            hotel_name = ' '.join(hotel_name)
            
            # To plot the hotel occupancies
            plt.plot(h[1], label= hotel_name)
            
            # To replace the hotel_name by the x_coord
            new_t = (x_coord, h[1])
            plot_info_copy.append(new_t)

        # To add the proper features
        plt.title("Occupancies for month of " + month)
        plt.xlabel("Day of month")
        plt.ylabel("Number of reservations")
        plt.legend()
        
        # To save the figure    
        plt.savefig("hotel_occupancies_" + month)
        
        return plot_info_copy
        




if __name__ == '__main__':
     doctest.testmod()
    
    # load_system
#     Reservation.booking_numbers = []
#     system = Booking.load_system()
#     print(len(system.hotels))
#     print(system.hotels[1].name)
#     print(print(system.hotels[1].rooms[314]))

    # menu
#     Reservation.booking_numbers = []    
#     booking = Booking.load_system()
#     booking.menu()
#     
    # create_reservation
#     Reservation.booking_numbers = []
#     random.seed(137)
#     booking = Booking.load_system()
#     booking.create_reservation()

    # cancel_reservation
#     Reservation.booking_numbers = []
#     booking = Booking.load_system()
#     booking.cancel_reservation() #9998701091820
#     booking.cancel_reservation() #9998701091820

    # look_up_reservation
#     Reservation.booking_numbers = []
#     booking = Booking.load_system()
#     booking.lookup_reservation() 


    # delete_reservations_at_random
#     Reservation.booking_numbers = []
#     random.seed(1338)
#     booking = Booking.load_system()
#     booking.delete_reservations_at_random()
#     print(len(booking.hotels[1].reservations))
#     print(len(booking.hotels[0].reservations))


    # plot_occupancies
#     Reservation.booking_numbers = []
#     booking = Booking.load_system()
#     booking.plot_occupancies('Oct')







