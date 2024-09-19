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
        company: str = input("Enter your company name: ").strip()

        if not firstname or not lastname or not company:
            raise ValueError("All fields are required.")


        # update company to a name without spaces and lowercase
        company = company.replace(" ", "_").lower()


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
            data[f"{firstname}_{lastname}"] = hashed_api_key
            # write updated data to the file
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)


        # generate mongo DataBase, collections and user with roles
        client = MongoClient(
                            host = "127.0.0.1",
                            port = 27017,
                            username = "root",
                            password = "root"
                        )
        
        with client:
            db = client[company]
            db.command("createUser",
                       f"{firstname}_{lastname}",
                       pwd=hashed_api_key,
                       roles=["readWrite"]
                       )
            
            db.create_collection("Quotes")
            db.create_collection("Invoices")
            db.create_collection("Companies")
            db.create_collection("Items")


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