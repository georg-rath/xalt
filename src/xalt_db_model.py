from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Index, Table, LargeBinary, ForeignKey, create_engine
from sqlalchemy.orm import relationship

__Base = declarative_base()

relation_assoc_link_object =  Table('join_link_object',
                                    __Base.metadata,
                                    Column('link_id', Integer, ForeignKey('xalt_link.link_id')),
                                    Column('obj_id', Integer, ForeignKey('xalt_object.obj_id'))
                              )

relation_assoc_run_object =  Table('join_run_object',
                                    __Base.metadata,
                                    Column('obj_id', Integer, ForeignKey('xalt_object.obj_id')),
                                    Column('run_id', Integer, ForeignKey('xalt_run.run_id'))
                              )

class XALT_link(__Base):
  __tablename__ = 'xalt_link'

  link_id = Column(Integer, primary_key=True)
  uuid = Column(String(length=36), nullable=False, unique=True)
  hash_id = Column(String(length=40), nullable=False)
  date = Column(DateTime, nullable=False)
  link_program = Column(String, nullable=False)
  build_user = Column(String(length=64), nullable=False)
  build_syshost = Column(String(length=64), nullable=False)
  build_epoch = Column(Float, nullable=False)
  exit_code = Column(Integer, nullable=False)
  exec_path = Column(String, nullable=False)
  objects = relationship('XALT_object', secondary=lambda: relation_assoc_link_object)

class XALT_run(__Base):
  __tablename__ = 'xalt_run'

  run_id = Column(Integer, primary_key=True)
  job_id = Column(String, nullable=False)
  run_uuid = Column(String(length=36), nullable=False)
  date  = Column(DateTime, nullable=False)
  syshost = Column(String(length=64), nullable=False) 
  uuid = Column(String(length=36), nullable=True) # TODO: should this be unique?
  hash_id = Column(String(length=40), nullable=False)
  account = Column(String, nullable=False)
  exec_type = Column(String(length=7), nullable=False)
  start_time = Column(Float, nullable=False)
  end_time = Column(Float, nullable=False)
  run_time = Column(Float, nullable=False)
  num_cores = Column(Integer, nullable=False)
  num_nodes = Column(Integer, nullable=False)
  num_threads = Column(Integer, nullable=False)
  queue = Column(String, nullable=False)
  exit_code = Column(Integer, nullable=False)
  user = Column(String(length=64), nullable=False)
  exec_path = Column(String, nullable=False)
  module_name = Column(String, nullable=True)
  cwd = Column(String, nullable=True)
  job_num_cores = Column(Integer, nullable=True)
   
  objects = relationship('XALT_object', secondary=relation_assoc_run_object)
  __table_args__ = ( Index('index_run_uuid', 'run_uuid'), Index('index_jobid_syshost', 'job_id', 'syshost') )

class XALT_object(__Base):
  __tablename__ = 'xalt_object'

  obj_id = Column(Integer, primary_key=True)
  object_path = Column(String, nullable=False)
  syshost = Column(String(length=64), nullable=False)
  hash_id = Column(String(length=40), nullable=False)
  module_name = Column(String, nullable=True)
  timestamp = Column(DateTime, nullable=True)
  lib_type = Column(String(length=2), nullable=False)
  links = relationship('XALT_link', secondary=lambda: relation_assoc_link_object) 
  runs = relationship('XALT_run', secondary=lambda: relation_assoc_run_object)
  
  __table_args__ = ( Index('index_hash_id', 'hash_id'), Index('index_objpath_hashid_syshost', 'object_path', 'hash_id', 'syshost') )

class XALT_env_name(__Base):
  __tablename__ = 'xalt_env_name'

  env_id = Column(Integer, primary_key=True)
  env_name = Column(String, nullable=False)

class XALT_job_id(__Base):
  __tablename__ = 'xalt_job_id'

  inc_id = Column(Integer, primary_key=True)
  job_id = Column(Integer, nullable=False)

class XALT_join_run_env(__Base):
  __tablename__ = 'join_run_env'

  join_id = Column(Integer, primary_key=True)
  env_id = Column(Integer,  ForeignKey('xalt_env_name.env_id'), nullable=False)
  run_id = Column(Integer, ForeignKey('xalt_run.run_id'), nullable=False)
  env_value = Column(LargeBinary, nullable=False)
  env_name = relationship('XALT_env_name')
  run = relationship('XALT_run')

def initialize_schema(engine):
  __Base.metadata.create_all(engine, checkfirst=True)