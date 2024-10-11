import json
from passlib.context import CryptContext
from pymongo import MongoClient
from uuid import uuid4

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
file_path = "./flask/api_keys.json"



def generate_api_key():
    print("API KEY GENERATOR:")
    try:
        # get informations
        firstname: str = input("Enter your firstname: ").strip()
        lastname: str = input("Enter your lastname: ").strip()
        base_company: str = input("Enter your company name: ").strip()

        if not firstname or not lastname or not base_company:
            raise ValueError("All fields are required.")


        # update company to a name without spaces and lowercase
        company = base_company.replace(" ", "_").lower()


        # generate key
        api_key: str = str(uuid4())
        hashed_api_key: str = pwd_context.hash(api_key)


        # Read existing data from the file
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("File not found or invalid JSON. Creating a new file...")
            data = {}
            with open(file_path, "w") as f:
                pass
        else:
            pass
        finally:
            # generate data to dump
            username = f"{firstname}_{lastname}"
            data[username] = {
                "username": username,
                "key": hashed_api_key,
                "company": company
            }

            # write updated data to the file
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)


        # generate mongo DataBase, collections and user with roles
        client = MongoClient(
                            host = "127.0.0.1",
                            port = 27017,
                            username = "root", # DEV - Change to a secure user
                            password = "root"  # DEV - Change to a secure password
                        )
        
        with client:
            db = client[company]
            db.command("createUser",
                       f"{firstname}_{lastname}",
                       pwd=api_key,
                       roles=["readWrite"],
                       customData={"company": company}
                       )
            
            db.create_collection("Quotes")
            db.create_collection("Invoices")
            db.create_collection("Company")
            db.create_collection("Items")
            db.create_collection("Clients")
            

            db.Company.insert_one({
                "name" : base_company
            })


    except ValueError as e:
        print(f"Error: {e}")


    else:
        # Display api key
        print("Keep your API KEY safe.")
        print(f"API KEY: {api_key}")

    finally:
        print("Exiting...")


if __name__ == '__main__':
    generate_api_key()