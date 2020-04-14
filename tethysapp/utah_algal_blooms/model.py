import os
import uuid
import json


def add_new_bloom(db_directory, location, type, severity, date):
    """
    Persist new dam.
    """
    # Serialize data to json
    new_bloom_id = uuid.uuid4()
    bloom_dict = {
        'id': str(new_bloom_id),
        'location': location,
        'type': type,
        'severity': severity,
        'date': date
    }

    bloom_json = json.dumps(bloom_dict)

    # Write to file in {{db_directory}}/blooms/{{uuid}}.json
    # Make blooms dir if it doesn't exist
    blooms_dir = os.path.join(db_directory, 'blooms')
    if not os.path.exists(blooms_dir):
        os.mkdir(blooms_dir)

    # Name of the file is its id
    file_name = str(new_bloom_id) + '.json'
    file_path = os.path.join(blooms_dir, file_name)

    # Write json
    with open(file_path, 'w') as f:
        f.write(bloom_json)
