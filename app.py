import os
import hashlib
from datetime import datetime
from sqlalchemy import create_engine, String, Integer, Column, DateTime

from sqlalchemy.orm import sessionmaker, declarative_base
import uuid
from plyer import notification
import time
import logging

logging.basicConfig(level=logging.WARNING, filename="logs.log", filemode='w')

directory_to_monitor = "C:\\Users\\Lancelot\\Desktop\\Checksum Monitoring app\\monitor"
def generate_uuid():
    result = uuid.uuid4()
    return str(result)

def convert_to_timestamp(time_raw):
    new_time  = str(datetime.fromtimestamp(time_raw).strftime("%Y-%m-%d %H:%M:%S"))
    return new_time
    

Base = declarative_base()

class file_values(Base):
    __tablename__ = "files"
    file_id = Column("id", String, primary_key=True, default = generate_uuid)
    file_path = Column("file_path", String, nullable=False, unique=True)
    hash_value = Column("hash_value", String, nullable=False)
    time_stamp  = Column("last_modified", String)
    
    def __init__(self, file_path, hash_value, time_stamp):
        self.file_path = file_path
        self.hash_value = hash_value
        self.time_stamp = time_stamp
        

db = "sqlite:///data.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def calculate_hash(file_path):
    with open(file_path, "rb") as file_obj:
        hash_value = hashlib.file_digest(file_obj, "sha256").hexdigest()
        
    return hash_value

def update_file_hashes():
    for root, dirs, files in os.walk(directory_to_monitor):
        for file in files:
            file_path = os.path.join(root, file)
            hash_value = calculate_hash(file_path)
            last_modified = os.path.getmtime(file_path)
            last_modified = convert_to_timestamp(last_modified)

            value = session.query(file_values).filter(file_values.file_path == file_path)
            if value.first() == None:
                session.add(file_values(file_path, hash_value, last_modified))
                session.commit()
            else:
                value.update({
                    "file_path": file_path,
                    "hash_value": hash_value,
                    "time_stamp": last_modified
                })
                session.commit()

def check_integrity():
    for root, dir, files in os.walk(directory_to_monitor):
        for file in files:
            file_path = os.path.join(root, file)
            current_hash = calculate_hash(file_path)
            result = session.query(file_values).filter(file_values.file_path == file_path)
            stored_hash = result.first().hash_value
            if result.first() == None:
                update_file_hashes()
            else:
                if stored_hash != current_hash:
                    logging.warning(f"FILE VIOLATION ON {file_path} at {convert_to_timestamp(os.path.getmtime(file_path))}")
                    notify_user(file_path, convert_to_timestamp(os.path.getmtime(file_path)))
                    update_file_hashes()
                else:
                    pass
                
                
def notify_user(file_path, last_modified):
    last_modified_str = last_modified
    notification_title = "File Integrity Violation Detected"
    notification_message = f"File integrity violation detected for file: {file_path}\nLast modified: {last_modified_str}"
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name="File Integrity Monitor",
        timeout=10
    )
    
if __name__ == "__main__":
    update_file_hashes()
    logging.info("STARTED RUNNING")

    while True:
        check_integrity()
        time.sleep(10)