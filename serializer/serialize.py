def decode_document(document, fields, id_field="_id") -> dict:
    """
    Decodes a MongoDB document to a dictionary with specific fields.
    
    Args:
        document: The MongoDB document to decode.
        fields: A list of field names to include in the resulting dictionary.
        id_field: The field name for the MongoDB ObjectId (defaults to "_id").
        
    Returns:
        A dictionary with the specified fields.
    """
    return {field: str(document.get(id_field)) if field == "id" else document.get(field) for field in fields}

def decode_documents(documents, fields, id_field="_id"):
    """
    Decodes multiple MongoDB documents.
    
    Args:
        documents: A list of MongoDB documents.
        fields: A list of field names to include in each decoded dictionary.
        id_field: The field name for the MongoDB ObjectId (defaults to "_id").
        
    Returns:
        A list of dictionaries with the specified fields.
    """
    return [decode_document(doc, fields, id_field) for doc in documents]

