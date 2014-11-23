from xalt_db_model import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime
engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

link1 = XALT_link(uuid='1234',
                  hash_id='1234',
                  date=datetime.now(),
                  link_program='abc',
                  build_user='hans',
                  build_syshost='hansis pc',
                  build_epoch = 23.0,
                  exit_code = 0,
                  exec_path = '/bin/bash')
object1 = XALT_object( 
  object_path = '/bin',
  syshost = 'yp',
  hash_id = 'blah',
  module_name = 'hans',
  timestamp = datetime.now(),
  lib_type = 'ld',
)
object1.links.append(link1)
session.add(link1)
session.add(object1)
session.flush()

