import re
def convert_drive_link(shareable_link):
    # Example of converting from "https://drive.google.com/file/d/FILE_ID/view?usp=sharing"
    # to "https://drive.google.com/uc?export=view&id=FILE_ID"
    match = re.search(r'/file/d/(.*?)/', shareable_link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    else:
        return None