from pymongo import IndexModel, ASCENDING, TEXT

# Define indexes for better query performance
COURT_INDEXES = [
    IndexModel([("name", TEXT)]),
    IndexModel([("address", TEXT)]),
    IndexModel([("surface", ASCENDING)]),
    IndexModel([("is_indoor", ASCENDING)]),
    IndexModel([("price_per_hour", ASCENDING)]),
    IndexModel([("created_by", ASCENDING)]),
    IndexModel([("createdAt", ASCENDING)]),
]
