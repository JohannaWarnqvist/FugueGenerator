from Fugue import Fugue

# Main program

key = 0
#fugue = Fugue(key)                 # Use random subject
fugue = Fugue(key, False, 2)        # Use test subject
    
fugue.print_fugue()
