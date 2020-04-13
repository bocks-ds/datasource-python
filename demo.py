from datasource_python import Client, DSQueryError, DSTargetError


client = Client("starfinder")

client.armor.set_arguments({"name_like":"basic"})
armor_by_name = client.armor.get(['name']) # Retrieves full response object & clears arguments
print(armor_by_name.json()) # Prints json response of items with 'basic' in their name.

print("-----")

client.armor.set_arguments({"price_min":200, "price_max":2000})
all_armor = client.armor.get(['name', 'price']).json()
print(all_armor) # Prints json response of all items with prices between 200 and 2000.

print("-----")

try:
    client.armor.set_arguments({"name_min":200, "name_max":2000})
    erroneous_armor = client.armor.get(['name', 'price']) # Throws exception due to errors in response.json()
except DSQueryError as e:
    print(e) # <Response 400> ['Unknown argument "name_min" on field "Query.armor". Did you mean "name_is", "name_like", "type_min", "bulk_min", or "level_min"?', 'Unknown argument "name_max" on field "Query.armor". Did you mean "name_is", "type_max", "bulk_max", "level_max", or "name_like"?']
    print(e.errors) # Same as above, but in list form (without "<Response 400>")
    print(e.status_code) # 400

print("-----")

try:
    client.bad_name.get(['name']).json()
except DSQueryError as e:
    print(e) # <Response 400> DataSource did not find table/field 'bad_name'.

print("-----")

try:
    bad_client = Client("bad_client")
except DSTargetError as e:
    print(e) # The target 'bad_client' provided in Client initialization is not in available target names:\n['starfinder', 'pathfinder']
