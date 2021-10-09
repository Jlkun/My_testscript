#! /usr/bin/python
# encoding=utf-8

import logging
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, TIMESTAMP

logger = logging.getLogger()

BaseModel = declarative_base()


class ModelMixin(object):
    def __repr__(self):
        dump_json = {}
        dump_json.update({'__class__': self.__class__.__name__})
        dump_json.update(self.__dict__)
        dump_json.__delitem__('_sa_instance_state')
        dump_str = '{\n'
        for key in sorted(dump_json.keys()):
            if not isinstance(dump_json[key], str):
                fmt = '"%s": %s\n'
            else:
                fmt = '"%s": "%s"\n'
            dump_str += fmt % (key, str(dump_json[key]))
        dump_str += '}\n'
        return dump_str


class WindAppUser(BaseModel):
    __tablename__ = 'tbl_wind_app_user'

    id = Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    app_user_id = Column(String(64))
    source = Column(String(64))
    phone = Column(String(64))
    status = Column(Integer)

    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)


class WindBizParam(BaseModel):
    __tablename__ = 'tbl_wind_biz_param'

    id = Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    biz_type = Column(Integer)
    biz_code = Column(String(64))
    param_key = Column(String(128))
    param_key_index =Column(String(32))
    param_value = Column(String(1024))
    param_desc = Column(String(64))
    param_level = Column(String(16))


    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)


class WindCardApply(BaseModel):
    __tablename__ = 'tbl_wind_card_apply'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    req_seq = Column(String(64))
    user_id = Column(Integer)
    partner_id = Column(Integer)
    card_type_id = Column(Integer)
    partner_token = Column(String(256))


    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)

class WindCardType(BaseModel):
    __tablename__ = 'tbl_wind_card_type'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    partner_id = Column(Integer)
    card_type_code =Column(String(64))
    name = Column(String(128))
    status = Column(Integer)


    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)

class WindIssueCardTask(BaseModel):
    __tablename__ = 'tbl_wind_issue_card_task'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    last_update_time = Column(TIMESTAMP)
    card_apply_id = Column(Integer)
    partner_id = Column(Integer)
    partner_token = Column(String(128))
    req_sys_code = Column(Integer)
    card_type_id = Column(Integer)
    sub_card_type_id = Column(Integer)
    status = Column(Integer)
    card_no = Column(String(64))
    app_code = Column(String(64))



    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)



class WindNotifyRecords(BaseModel):
    __tablename__ = 'tbl_wind_notify_records'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    last_update_time = Column(TIMESTAMP)
    status = Column(Integer)
    notify_sys_code = Column(String(128))
    co_card_type_code = Column(String(64))
    sub_card_type_code = Column(String(64))
    card_no = Column(String(64))
    type = Column(Integer)
    partner_token = Column(String(512))
    issue_card_task_id = Column(Integer)
    user_card_id = Column(Integer)
    remark = Column(String(64))


    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)


class WindPartner(BaseModel):
    __tablename__ = 'tbl_wind_partner'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    name = Column(String(128))
    partner_no = Column(String(64))
    status = Column(Integer)

    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)

class WindSubCardType(BaseModel):
    __tablename__ = 'tbl_wind_sub_card_type'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    partner_id = Column(Integer)
    card_type_id = Column(Integer)
    status = Column(Integer)
    sub_card_type_code = Column(String(64))
    name = Column(String(128))
    medal = Column(String(128))
    skin_id = Column(String(64))
    face_sys_code = Column(String(64))




    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)

class WindSysParam(BaseModel):
    __tablename__ = 'tbl_wind_sys_param'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    para_key = Column(String(128))
    para_desc = Column(String(512))
    para_value = Column(String(1024))


    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)

class WindUpdateFaceRecords(BaseModel):
    __tablename__ = 'tbl_wind_update_face_records'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    last_update_time = Column(TIMESTAMP)
    skin_id = Column(String(64))
    status = Column(Integer)
    card_no = Column(String(64))
    face_sys_code = Column(String(64))
    issue_card_task_id = Column(Integer)
    user_card_id = Column(Integer)

    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)

class WindUserCard(BaseModel):
    __tablename__ = 'tbl_wind_user_card'
    id =Column(Integer, Sequence('seq_order', start=1, increment=1), primary_key=True)
    create_time = Column(TIMESTAMP)
    last_update_time = Column(TIMESTAMP)
    issue_card_task_id = Column(Integer)
    partner_user_id = Column(String(128))
    extra_data = Column(String(512))
    issue_data = Column(String(512))
    partner_data = Column(String(512))
    status = Column(Integer)
    bind_flag = Column(Integer)
    partner_id = Column(Integer)
    sub_card_type_id = Column(Integer)
    card_no = Column(String(64))



    def list_all_member(self):
        vars(self).pop('_sa_instance_state')
        for name, value in vars(self).items():
            try:
                logger.info('%s=%s' % (name, value.decode('utf8')))
            except AttributeError:
                logger.info('%s=%s' % (name, value))
        return vars(self)