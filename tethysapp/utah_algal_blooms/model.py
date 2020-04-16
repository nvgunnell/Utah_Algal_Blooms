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


def get_all_blooms(db_directory):
    """
    Get all persisted blooms.
    """
    # Write to file in {{db_directory}}/blooms/{{uuid}}.json
    # Make blooms dir if it doesn't exist
    blooms_dir = os.path.join(db_directory, 'blooms')
    if not os.path.exists(blooms_dir):
        os.mkdir(blooms_dir)

    blooms = []

    # Open each file and convert contents to python objects
    for bloom_json in os.listdir(blooms_dir):
        # Make sure we are only looking at json files
        if '.json' not in bloom_json:
            continue

        bloom_json_path = os.path.join(blooms_dir, bloom_json)
        with open(bloom_json_path, 'r') as f:
            bloom_dict = json.loads(f.readlines()[0])
            blooms.append(bloom_dict)

    return blooms