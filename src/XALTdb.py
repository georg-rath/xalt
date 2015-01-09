#-----------------------------------------------------------------------
# XALT: A tool that tracks users jobs and environments on a cluster.
# Copyright (C) 2013-2014 University of Texas at Austin
# Copyright (C) 2013-2014 University of Tennessee
# 
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of 
# the License, or (at your option) any later version. 
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser  General Public License for more details. 
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307 USA
#-----------------------------------------------------------------------

from __future__ import print_function
import os, sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

dirNm, execName = os.path.split(os.path.realpath(sys.argv[0]))
sys.path.append(os.path.realpath(os.path.join(dirNm, "../libexec")))
sys.path.append(os.path.realpath(os.path.join(dirNm, "../site")))

import ConfigParser
from   xalt_util     import *
from   xalt_site_pkg import translate
from xalt_db_model import *
from sqlalchemy import and_

def convertToInt(s):
  """
  Convert to string to int.  Protect against bad input.
  @param s: Input string
  @return: integer value.  If bad return 0.
  """
  try:
    value = int(s)
  except ValueError:
    value = 0
  return value

patSQ = re.compile("'")
class XALTdb(object):
  """
  This XALTdb class opens the XALT database and is responsible for
  all the database interactions.
  """
  def __init__(self, configFile):
    """ Initialize the class and save the db config file. """
    self.__connection_string = None
    self.__sessionmaker = None

    try:
      config=ConfigParser.ConfigParser()
      config.read(configFile)
      self.__connection_string    = config.get("DATABASE","CONNECTION_STRING")
    except ConfigParser.Error, err:
        raise err

  def connect(self):
    """
    Public interface to connect to DB.
    
    """
    try:
        if self.__sessionmaker is None:
          engine = create_engine(self.__connection_string)
          initialize_schema(engine)
          self.__sessionmaker = sessionmaker(bind=engine)

    except SQLAlchemyError, e:
      print ("XALTdb: Error %d: %s" % (e.args[0], e.args[1]), file=sys.stderr)
      raise

    return self.__sessionmaker

  def connection_string(self):
    """ Return connection string"""
    return self.__connection_string

  def link_to_db(self, reverseMapT, linkT):
    """
    Stores the link table data into the XALT db
    @param reverseMapT: The reverse map table that maps directories to modules
    @param linkT:       The table that contains the link data.
    """
    try:
        if self.__sessionmaker is None:
            self.connect()
        session = self.__sessionmaker()

        # check if linkT['uuid'] already in db - if yes: do nothing
        db_link = session.query(XALT_link).filter(XALT_link.uuid == linkT['uuid']).scalar()
        if db_link is None:
            db_link = XALT_link(
                uuid = linkT['uuid'],
                hash_id = linkT['hash_id'],
                link_program = linkT['link_program'],
                build_user = linkT['build_user'],
                build_syshost = linkT['build_syshost'],
                build_epoch = float(linkT['build_epoch']),
                date = datetime.fromtimestamp(float(linkT['build_epoch'])),
                exit_code = convertToInt(linkT['exit_code']),
                exec_path = patSQ.sub(r"\\'", linkT['exec_path'])
            )

            for obj in linkT['linkA']:
              object_path = obj[0]
              hash_id = obj[1]

              # for each linkT['linkA']:
              #   - load object id -> if exist use, if not exist -> create
              db_obj = session.query(XALT_object).filter(and_(
                                    XALT_object.hash_id == hash_id,
                                    XALT_object.object_path == object_path,
                                    XALT_object.syshost ==  linkT['build_syshost'])).scalar()
              if db_obj is None:
                db_obj = XALT_object(
                    hash_id = hash_id,
                    object_path = object_path,
                    syshost = linkT['build_syshost'],
                    module_name = obj2module(object_path, reverseMapT),
                    timestamp = datetime.now(),
                    lib_type = obj_type(object_path)
                )
              db_link.objects.append(db_obj)
              session.add(db_obj)
            session.add(db_link)
            session.commit()
    except Exception as e:
      print ("link_to_db(): Error ",e)
      sys.exit (1)

  def run_to_db(self, reverseMapT, runT):
    """
    Store the "run" data into the database.
    @param: reverseMapT: The map between directories and modules
    @param: runT:        The run data stored in a table
    """

    nameA = [ 'num_cores', 'num_nodes', 'account', 'job_id', 'queue' , 'submit_host']
    try:
      # ORM: open connex
      if self.__sessionmaker is None:
        self.connect()
      session = self.__sessionmaker()

      translate(nameA, runT['envT'], runT['userT'])
      dateTimeStr = datetime.fromtimestamp(float(runT['userT']['start_time']))
      uuid = runT['xaltLinkT'].get('Build.UUID')
      if (uuid):
        uuid = "'" + uuid + "'"
      else:
        uuid = "NULL"


      db_run = session.query(XALT_run).filter(XALT_run.run_uuid == runT['userT']['run_uuid']).scalar()

      if db_run is not None:
        db_run.run_time = runT['userT']['run_time']
        db_run.end_time = runT['userT']['end_time']
      else:
        moduleName  = obj2module(runT['userT']['exec_path'], reverseMapT)
        exit_status = runT['userT'].get('exit_status',0)
        job_num_cores = int(runT['userT'].get('job_num_cores',0))

        db_run = XALT_run(
              run_uuid = runT['userT']['run_uuid'],
              job_id = runT['userT']['job_id'],
              date = dateTimeStr,
              syshost = runT['userT']['syshost'],
              uuid = uuid,
              hash_id = runT['hash_id'],
              account = runT['userT']['account'],
              exec_type = runT['userT']['exec_type'],
              start_time = runT['userT']['start_time'],
              end_time = runT['userT']['end_time'],
              run_time = runT['userT']['run_time'],
              num_cores = runT['userT']['num_cores'],
              num_nodes = runT['userT']['num_nodes'],
              num_threads = runT['userT']['num_threads'],
              queue = runT['userT']['queue'],
              exit_code = exit_status,
              user = runT['userT']['user'],
              exec_path = runT['userT']['exec_path'],
              module_name = moduleName,
              cwd = runT['userT']['cwd'],
              job_num_cores = job_num_cores
          )

        for obj in runT['libA']:
          object_path = obj[0]
          hash_id = obj[1]

          # for each runT['libA']:
          #   - load object id -> if exist use, if not exist -> create
          db_obj = session.query(XALT_object).filter(and_(
            XALT_object.hash_id == hash_id,
            XALT_object.object_path == object_path,
            XALT_object.syshost == runT['userT']['syshost'])).scalar()
          if db_obj is None:
            db_obj = XALT_object(
                hash_id = hash_id,
                object_path = object_path,
                syshost = runT['userT']['syshost'],
                module_name = obj2module(object_path, reverseMapT),
                timestamp = datetime.now(),
                lib_type = obj_type(object_path)
            )
          db_run.objects.append(db_obj)
          session.add(db_obj)
      session.add(db_run)

      for key in runT['envT']:
        # use the single quote pattern to protect all the single quotes in env vars.
        value = patSQ.sub(r"\\'", runT['envT'][key])
        db_env = session.query(XALT_env_name).filter(XALT_env_name.env_name == key).scalar()
        if db_env is None:
          db_env = XALT_env_name(env_name = key)

        db_join_run_env = XALT_join_run_env(
            run = db_run,
            env_name = db_env,
            env_value = value.encode("ascii","ignore")
        )

        session.add(db_env)
        session.add(db_join_run_env)

      session.commit()

    except Exception as e:
      print ("run_to_db(): ", e)
      sys.exit (1)
