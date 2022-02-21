
def resolve_metadata(metadata, section, _id):
    """Return metdata value in a given section of metadata and given id"""
    for i in metadata[section]:
        if i['id'] == _id:
            return i['name']
    return None