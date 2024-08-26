import os
import json
import pandas as pd

# Get the current directory
current_dir = os.getcwd()

# Define the directory where the JSON files are located
json_dir = os.path.join(current_dir, 'CarTravel/data_process/database/hotel_data')


df = pd.DataFrame(columns=['Hotel Name', 'priceRange', 'reviewCount'])
num_have_reviews = 0
num_have_priceRange = 0
hotels_have_reviews = []
num_have_des_no_price = 0

# Iterate over each file in the directory
for i, filename in enumerate(os.listdir(json_dir)):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Open the JSON file
        with open(os.path.join(json_dir, filename), 'r') as f:
            print("Looking at: " + filename + "...")
            
            # Load the JSON data
            data = json.load(f)
            
            # Check if 'priceRange' exists and if there's at least one review
            if 'priceRange' in data['basic_data']:
                if 'aggregateRating' in data['basic_data']:
                    new_row = pd.DataFrame({
                        'Hotel Name': data['basic_data']['name'],
                        'priceRange': data['basic_data']['priceRange'],
                        'reviewCount': data['basic_data']['aggregateRating']['reviewCount']
                    }, index=[i])
                    num_have_reviews += 1
                    
                # else:
                #     json_file_path = json_dir + '/' + filename
                #     os.remove(json_file_path)
                #     print("Removed: " + filename)
                    
                df = pd.concat([df, new_row], ignore_index=True)
                num_have_priceRange += 1
                
            else:
                if 'description' in data:
                    if 'aggregateRating' in data['basic_data']:
                        new_row = pd.DataFrame({
                            'Hotel Name': data['basic_data']['name'],
                            'priceRange': 'null',
                            'reviewCount': data['basic_data']['aggregateRating']['reviewCount']
                        }, index=[i])
                        num_have_reviews += 1
                        num_have_des_no_price += 1
                    # else:
                    #     json_file_path = json_dir + '/' + filename
                    #     os.remove(json_file_path)
                    #     print("Removed: " + filename)
                # else:    
                #     json_file_path = json_dir + '/' + filename
                #     os.remove(json_file_path)
                #     print("Removed: " + filename)

# Print the DataFrame
print(df)
print("\nstats:")
print("total number of json: " + str(i+1))
print("num_have_priceRange: " + str(num_have_priceRange))
print("num_have_reviews: " + str(num_have_reviews))
print("num_have_description_no_price: " + str(num_have_des_no_price))