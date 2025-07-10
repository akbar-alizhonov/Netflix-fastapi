import uuid


def generate_filename_and_path(content_type: str):
    file_ext = content_type.split('/')[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    path = "/images/"

    return filename, path
