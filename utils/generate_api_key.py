#utils/generate_api_key.py


# Lib
import getpass
from passlib.context import CryptContext
from pymongo import MongoClient, errors
from uuid import uuid4



# Vars
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# Functions
def get_mongodb_connexion() -> MongoClient:

    print("MongoDB connexion requires credentials..")
    print("Enter the following credentials and mongoDB connexion informations:")
    mongo_host = input("Enter your MongoDB host (default: localhost): ").strip() or "localhost"
    mongo_port = input("Enter your MongoDB port (default: 27017): ").strip() or "27017"
    mongo_user = input("Enter your MongoDB username (default: root): ").strip() or "root"
    mongo_password = getpass.getpass("Enter your MongoDB password (default: root): ").strip() or "root"


    print(f"host: {mongo_host}, port: {mongo_port}, username: {mongo_user}")


    client = MongoClient(
                        host = mongo_host,
                        port = int(mongo_port),
                        username = mongo_user,
                        password = mongo_password,
                        authSource = "admin"
                        )
    
    try:
        client.admin.command('ismaster')
        print("MongoDB connection successful.")
        return client
    
    except errors.ConnectionFailure as e:
        raise ValueError(f"MongoDB not available. Error: {e}")





def generate_api_key() -> dict:

    print("\n")
    print("Enter the following informations to generate an API KEY:")
    firstname: str = input("Enter your firstname: ").strip()
    lastname: str = input("Enter your lastname: ").strip()
    company: str = input("Enter your company name: ").strip()

    if not firstname or not lastname or not company:
        raise ValueError("All fields are required. Exiting..")


    company = company.replace(" ", "_").lower()

    api_key: str = str(uuid4())
    hashed_api_key: str = pwd_context.hash(api_key)

    print("\n")
    print("API KEY GENERATED:")
    print(f"API KEY: {api_key}")
    print("Keep your API KEY safe, it can't be recovered.")

    user_data: dict = {
        "username": f"{firstname}_{lastname}",
        "password": hashed_api_key,
        "company": company
    }

    return user_data



def insert_user_in_db(client: MongoClient, user_data:dict):

    db = client["users"]

    try:
        db.create_collection("user_data")

    except errors.CollectionInvalid:
        pass

    finally:
        collection = db["user_data"]


        collection.insert_one({
                    "username" : user_data["username"],
                    "password" : user_data["password"],
                    "company" : user_data["company"]
                })

        print("User data inserted in MongoDB.")




if __name__ == '__main__':
    
    print("API KEY GENERATOR:")

    client = get_mongodb_connexion()
    user_data = generate_api_key()

    insert_user_in_db(client, user_data)

    print("Exiting...")