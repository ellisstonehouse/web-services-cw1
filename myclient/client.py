import requests


def register():
    url = input("Enter the URL: ")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")

    try:
        response = session.get(url+"/register",
                               params={"username": username,
                                       "password": password,
                                       "email": email}).json()
            

        print(response["response"])

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def login(url):

    global base_url

    username = input("Username: ")
    password = input("Password: ")

    try:
        response = session.get(url+"/login",
                               params={"username": username,
                                       "password": password})
        
        if response.status_code == 200:
            base_url = url

        r = response.json()

        print(r["response"])
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def logout():

    global base_url

    try:
        response = session.get(base_url+"logout")

        base_url = ""

        r = response.json()

        print(r["response"])

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please check the URL.")
    except requests.exceptions.RequestException:
        print(f"Error: Not logged in")

def list():
    try:
        response = session.get(base_url+"/list")

        r = response.json()

        if response.status_code == 200:

            for i in r["response"]:
                print(f"Module: {i['module_ID']}, {i['module_name']}")
                print(f"Year: {i['year']}")
                print(f"Semester: {i['semester']}")
                print("Professors:")

                for prof_id, prof_name in zip(i["professor_ids"], i["professor_names"]):
                    print(f"  - {prof_id}, {prof_name}")

                print("-" * 40)  # Separator
        else:
            print(r["response"])
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please check the URL.")
    except requests.exceptions.RequestException:
        print("Error: Not logged in")

def view():
    try:
        response = session.get(base_url+"/view")
        
        r = response.json()

        if response.status_code == 200:

            for i in r["response"]:
                print(f"The rating of {i['professor_name']} ({i['professor_ID']}) is {i['avg_rating']}")
        else:
            print(r["response"])
    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please check the URL.")
    except requests.exceptions.RequestException:
        print("Error: Not logged in")


def average(professor_id, module_id):
    try:
        response = session.get(base_url+"/average",
                               params={"professor_id": professor_id,
                                       "module_id": module_id})
        
        r = response.json()

        if response.status_code == 200:

            if r['avg_rating'] == None:
                print(f"No ratings found for Professor {r['professor_name']} ({r['professor_ID']}) in module {r['module_name']} {r['module_ID']}'")
            else:
                print(f"The rating of {r['professor_name']} ({r['professor_ID']}) in module {r['module_name']} {r['module_ID']} is {r['avg_rating']}")
        else:
            print(r["response"])

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please check the URL.")
    except requests.exceptions.RequestException:
        print("Error: Not logged in")


def rate(professor_id, module_id, year, semester, rating):
    try:
        response = session.get(base_url+"/rate", 
                                params={"professor_id": professor_id,
                                        "module_id": module_id,
                                        "year": year,
                                        "semester": semester,
                                        "rating": rating})
        
        r = response.json()

        print(r["response"])

    
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please check the URL.")
    except requests.exceptions.RequestException:
        print("Error: Not logged in")


if __name__ == "__main__":

    base_url = ""

    session = requests.Session() # so the client is remembered after login

    while True:

        cmd = input("Enter command (or 'exit' to quit): ").split()

        if cmd[0].lower() == "exit" or cmd[0].lower() == "quit":
            break

        elif cmd[0].lower() == "register":
            if len(cmd) == 1: register()
            else: print("Syntax: register\n")

        elif cmd[0].lower() == "login":
            if len(cmd) == 2: login(cmd[1])
            else: print("Syntax: login <url>\n")

        elif cmd[0].lower() == "list":
            if len(cmd) == 1: list()
            else: print("Syntax: list\n")

        elif cmd[0].lower() == "view":
            if len(cmd) == 1: view()
            else: print("Syntax: view\n")

        elif cmd[0].lower() == "average":
            if len(cmd) == 3: average(cmd[1], cmd[2])
            else: print("Syntax: average <professor_id> <module_code>\n")

        elif cmd[0].lower() == "rate":
            if len(cmd) == 6: rate(cmd[1], cmd[2], cmd[3], cmd[4], cmd[5])
            else: print("Syntax: rate <professor_id> <module_id> <year> <semester> <rating>\n")

        elif cmd[0].lower() == "logout":
            if len(cmd) == 1: logout()
            else: print("Syntax: logout\n")

        else:
            print("Invalid command\n")



