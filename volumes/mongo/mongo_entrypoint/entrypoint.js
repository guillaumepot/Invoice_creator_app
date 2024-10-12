// API User
print("Running entrypoint.js script...");

db = db.getSiblingDB('admin');


// Check if the user already exists
const user = db.getUser("api");
if (!user) {
    // Create the user if it does not exist
    db.createUser({
        user: "api",
        pwd: "api",
        roles: [
            {
                role: "readAnyDatabase",
                db: "admin"
            },
            {
                role: "dbAdminAnyDatabase",
                db: "admin"
            },
            {
                role: "userAdminAnyDatabase",
                db: "admin"
            },
            {
                role: "readWrite",
                db: "users"
            }
        ]
    });
    print("User 'api' created successfully.");
} else {
    print("User 'api' already exists, skipping.");
}