import gspread
import getpass

while True:
    # Ask user to login
    username = raw_input("Enter your Drive email address: ")
    password = getpass.getpass("Enter Password: ")

    try:
        # Authenticate user
        gc = gspread.login(username, password)
        break;
    except gspread.exceptions.AuthenticationError:
        print ">> Login failed! Try again...\n"

# OR replace everything above with below (uncommented)
# using your email address and password explicitely
'''
gc = gspread.login(yourEmail, yourPassword)
'''

# Open the required spreadsheet
sheet = gc.open("DNS").sheet1

# Create the zone file and start writing to it
zone = open('zone.txt', 'w')

# Start of zone file
zone.write("$ORIGIN " + sheet.row_values(1)[0] + "\n")

# TTL
zone.write("$TTL " + sheet.row_values(2)[0] + "\n")

# All the Resource Records
for x in range(3, len(sheet.get_all_values())+1):
    # Fetch row
    row = sheet.row_values(x)

    # Check for blank record owners
    if(row[0] is None):
        row[0] = ''
            
    # Write RR to file
    zone.write(row[0] + "\t" + row[1] + "\t" + row[2] + "\t" + row[3] + "\n")

zone.close()
