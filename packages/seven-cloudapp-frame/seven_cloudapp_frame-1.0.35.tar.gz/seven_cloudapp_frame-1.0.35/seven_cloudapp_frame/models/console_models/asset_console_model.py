# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-07-19 13:37:16
@LastEditTime: 2022-07-20 14:52:10
@LastEditors: HuangJianYi
@Description: 
"""
import threading, multiprocessing
from seven_framework.console.base_console import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.db_models.asset.asset_inventory_model import *
from seven_cloudapp_frame.models.db_models.asset.asset_warn_notice_model import *
from seven_cloudapp_frame.models.db_models.asset.asset_log_model import *



class AssetConsoleModel():
    """
    :description: 资产控制台业务模型
    """
    def console_asset(self, mod_count=1):
        """
        :description: 控制台资产预警
        :param mod_count: 单表队列数
        :return: 
        :last_editors: HuangJianYi
        """
        sub_table_config_list = config.get_value("sub_table_config_list", {})
        sub_table_config = sub_table_config_list.get("asset_log_tb", {"sub_count": 0, "sub_ways": 0})
        sub_count = sub_table_config.get("sub_count", 0)
        if sub_count == 0:
            y = threading.Thread(target=self._process_user_asset_warn, args=[None])
            y.start()
        else:
            for i in range(sub_count):
                 o = threading.Thread(target=self._process_user_asset_warn, args=[str(i)])
                 o.start()

        for i in range(mod_count):
            j = threading.Thread(target=self._process_asset_inventory_warn, args=[i, mod_count])
            j.start()

        n = threading.Thread(target=self._process_asset_inventory_queue, args=[])
        n.start()

        l = threading.Thread(target=self._process_onlyid_warn, args=[])
        l.start()

        k = threading.Thread(target=self._push_warn_notice, args=[])
        k.start()

        t = threading.Thread(target=self._process_asset_intercept_queue, args=[])
        t.start()
        
    def _process_user_asset_warn(self, sub_table):
        """
        :description: 处理用户资产负数预警
        :param sub_table: 分表名称
        :return: 
        :last_editors: HuangJianYi
        """
        print(f"{TimeHelper.get_now_format_time()} 用户资产负数预警启动")
        while True:
            try:
                time.sleep(0.1)
                asset_log_model = AssetLogModel(sub_table=sub_table)
                asset_warn_notice_model = AssetWarnNoticeModel()
                now_date = TimeHelper.get_now_format_time()
                now_day_int = SevenHelper.get_now_day_int()
                asset_log_list = asset_log_model.get_list(f"now_value<0 and {now_day_int}>warn_day ", order_by="create_date asc", limit="100")
                if len(asset_log_list) > 0:
                    for asset_log in asset_log_list:
                        try:
                            asset_log.warn_date = now_date
                            asset_log.warn_day = now_day_int
                            asset_log_model.update_entity(asset_log, "warn_date,warn_day")

                            asset_warn_notice = AssetWarnNotice()
                            asset_warn_notice.app_id = asset_log.app_id
                            asset_warn_notice.act_id = asset_log.act_id
                            asset_warn_notice.handler_name = asset_log.handler_name
                            asset_warn_notice.request_code = asset_log.request_code
                            asset_warn_notice.user_id = asset_log.user_id
                            asset_warn_notice.open_id = asset_log.open_id
                            asset_warn_notice.user_nick = asset_log.user_nick
                            asset_warn_notice.asset_type = asset_log.asset_type
                            asset_warn_notice.asset_object_id = asset_log.asset_object_id
                            if asset_log.asset_type == 1:
                                asset_warn_notice.log_title = "次数异常"
                                asset_warn_notice.info_desc = f"值为负数:{asset_log.now_value}"
                            elif asset_log.asset_type == 2:
                                asset_warn_notice.log_title = "积分异常"
                                asset_warn_notice.info_desc = f"值为负数:{asset_log.now_value}"
                            elif asset_log.asset_type == 3:
                                asset_warn_notice.log_title = f"价格档位异常"
                                asset_warn_notice.info_desc = f"档位ID:{asset_log.asset_object_id},值为负数:{asset_log.now_value}"
                            else:
                                asset_warn_notice.log_title = f"资产类型：{asset_log.asset_type}异常"
                                asset_warn_notice.info_desc = f"值为负数:{asset_log.now_value}"

                            asset_warn_notice.info_json = SevenHelper.json_dumps(asset_log)
                            asset_warn_notice.create_date = now_date
                            asset_warn_notice.create_day = now_day_int
                            asset_warn_notice_model.add_entity(asset_warn_notice)

                        except Exception as ex:
                            logger_error.error(f"用户资产负数预警异常,json串:{SevenHelper.json_dumps(asset_log)},ex:{traceback.format_exc()}")
                            continue
                else:
                    time.sleep(1)
            except Exception as ex:
                time.sleep(5)

    def _process_onlyid_warn(self):
        """
        :description: 处理唯一值并发预警
        :return: 
        :last_editors: HuangJianYi
        """
        while True:
            try:
                time.sleep(0.1)
                asset_warn_notice_model = AssetWarnNoticeModel()
                redis_init = SevenHelper.redis_init()
                hash_name_1 = f"warn_handler_list_{str(SevenHelper.get_now_int(fmt='%Y%m%d'))}"
                hkeys = redis_init.hkeys(hash_name_1)
                if len(hkeys)<=0:
                    time.sleep(1)
                    continue
                for key in hkeys:
                    date_start = TimeHelper.format_time_to_datetime(format='%Y-%m-%d %H:%M')
                    date_end = date_start + datetime.timedelta(minutes=5)
                    date_list = []
                    while date_start < date_end:
                        date_list.append(str(TimeHelper.datetime_to_format_time(date_start, '%Y%m%d%H%M')))
                        date_start += datetime.timedelta(minutes=1)
                    hash_name_2 = f"{hash_name_1}:{key}"
                    value_list = redis_init.hmget(hash_name_2,date_list)
                    if not value_list or len(value_list)<=0:
                        continue
                    count = 0
                    for value in value_list:
                        count += int(value)
                    if count <= 0:
                        continue
                    hash_value_1 = redis_init.hget(hash_name_1,key)
                    hash_value_1 = SevenHelper.json_loads(hash_value_1) if hash_value_1 else {"app_id":"","handler_name":""}
                    asset_warn_notice = AssetWarnNotice()
                    asset_warn_notice.app_id = hash_value_1["app_id"]
                    asset_warn_notice.act_id = 0
                    asset_warn_notice.ascription_type = 2
                    asset_warn_notice.handler_name = hash_value_1["handler_name"]
                    asset_warn_notice.request_code =""
                    asset_warn_notice.user_id = ""
                    asset_warn_notice.open_id = ""
                    asset_warn_notice.user_nick = ""
                    asset_warn_notice.asset_type = 0
                    asset_warn_notice.asset_object_id = ""
                    asset_warn_notice.log_title = "重复请求拦截"
                    asset_warn_notice.info_desc = f"{date_start}-{date_end}进行了{count}次拦截"
                    asset_warn_notice.info_json = {}
                    asset_warn_notice.create_date = SevenHelper.get_now_datetime()
                    asset_warn_notice.create_day = SevenHelper.get_now_day_int()
                    asset_warn_notice_model.add_entity(asset_warn_notice)
                time.sleep(5*60)
            except Exception as ex:
                time.sleep(5)

    def _push_warn_notice(self):
        """
        :description: 推送预警通知到消息系统
        :return: 
        :last_editors: HuangJianYi
        """
        while True:
            try:
                time.sleep(0.1)
                asset_warn_notice_model = AssetWarnNoticeModel()
                message_system_db = int(config.get_value("message_system_db",100))
                redis_init = SevenHelper.redis_init(message_system_db)
                warn_notice_list = asset_warn_notice_model.get_list("is_notice=0 and ascription_type=1",order_by="create_date asc",limit="50")
                if len(warn_notice_list) > 0:
                    for warn_notice in warn_notice_list:
                        try:
                            push_message = {}
                            push_message["project_id"] = int(config.get_value("project_name",0))
                            push_message["app_id"] = warn_notice.app_id
                            push_message["action_id"] = warn_notice.act_id
                            push_message["taobao_nick_name"] = warn_notice.user_nick
                            push_message["error_type"] = warn_notice.log_title
                            push_message["error_message"] = warn_notice.info_desc
                            push_message["handler"] = warn_notice.handler_name
                            redis_init.lpush("warning_notice_queue", JsonHelper.json_dumps(push_message))
                            warn_notice.is_notice = 1
                            warn_notice.notice_date = SevenHelper.get_now_datetime()
                            asset_warn_notice_model.update_entity(warn_notice,"is_notice,notice_date")
                        except Exception as ex:
                            logger_error.error(f"推送预警通知异常,json串:{SevenHelper.json_dumps(warn_notice)},ex:{traceback.format_exc()}")
                            continue
                time.sleep(1)
            except Exception as ex:
                time.sleep(5)

    def _process_asset_inventory_warn(self, mod_value, mod_count):
        """
        :description: 处理资产每日进销存是否对等预警
        :param mod_value: 当前队列值
        :param mod_count: 队列数
        :return: 
        :last_editors: HuangJianYi
        """
        print(f"{TimeHelper.get_now_format_time()} 资产每日进销存预警队列{mod_value}启动")
        while True:
            try:
                time.sleep(0.1)
                asset_inventory_model = AssetInventoryModel()
                asset_warn_notice_model = AssetWarnNoticeModel()
                now_date = TimeHelper.get_now_format_time()
                now_day_int = SevenHelper.get_now_day_int()
                if mod_count == 1:
                    asset_inventory_list = asset_inventory_model.get_list(f"create_day={now_day_int} and process_count=0", order_by="create_date asc", limit="100")
                else:
                    asset_inventory_list = asset_inventory_model.get_list(f"MOD(user_id,{mod_count})={mod_value} and create_day={now_day_int} and process_count=0", order_by="create_date asc", limit="100")
                if len(asset_inventory_list) > 0:
                    for asset_inventory in asset_inventory_list:
                        try:
                            asset_inventory.process_count = 1
                            asset_inventory.process_date = now_date
                            asset_inventory_model.update_entity(asset_inventory, "process_count,process_date")

                            if (asset_inventory.history_value + asset_inventory.inc_value + asset_inventory.dec_value) != asset_inventory.now_value:

                                asset_warn_notice = AssetWarnNotice()
                                asset_warn_notice.app_id = asset_inventory.app_id
                                asset_warn_notice.act_id = asset_inventory.act_id
                                asset_warn_notice.handler_name = ""
                                asset_warn_notice.request_code = ""
                                asset_warn_notice.user_id = asset_inventory.user_id
                                asset_warn_notice.open_id = asset_inventory.open_id
                                asset_warn_notice.user_nick = asset_inventory.user_nick
                                asset_warn_notice.asset_type = asset_inventory.asset_type
                                asset_warn_notice.asset_object_id = asset_inventory.asset_object_id
                                asset_warn_notice.info_desc = f"历史值:{asset_inventory.history_value},增加：{asset_inventory.inc_value},减少：{asset_inventory.dec_value},当前值:{asset_inventory.now_value}"
                                if asset_inventory.asset_type == 1:
                                    asset_warn_notice.log_title = "次数进销存异常"
                                elif asset_inventory.asset_type == 2:
                                    asset_warn_notice.log_title = "积分进销存异常"
                                elif asset_inventory.asset_type == 3:
                                    asset_warn_notice.log_title = "价格档位进销存异常"
                                    asset_warn_notice.info_desc = f"档位ID:{asset_inventory.asset_object_id}," + asset_warn_notice.info_desc
                                else:
                                    asset_warn_notice.log_title = f"资产类型：{asset_inventory.asset_type}异常"
                                asset_warn_notice.info_json = SevenHelper.json_dumps(asset_inventory)
                                asset_warn_notice.create_date = now_date
                                asset_warn_notice.create_day = now_day_int
                                asset_warn_notice_model.add_entity(asset_warn_notice)

                        except Exception as ex:
                            logger_error.error(f"资产每日进销存预警队列{mod_value}异常,json串:{SevenHelper.json_dumps(asset_inventory)},ex:{traceback.format_exc()}")
                            continue
                else:
                    time.sleep(60 * 60)
            except Exception as ex:
                time.sleep(5)

    def _process_asset_inventory_queue(self):
        """
        :description: 处理资产队列入进销存
        :return: 
        :last_editors: HuangJianYi
        """
        while True:
            try:
                time.sleep(0.1)
                redis_init = SevenHelper.redis_init()
                asset_inventory_model = AssetInventoryModel()
                asset_queue_json = redis_init.lpop(f"asset_queue_list")
                if not asset_queue_json:
                    time.sleep(1)
                    continue
                asset_queue_dict = SevenHelper.json_loads(asset_queue_json)
                try:
                    old_asset_inventory_id = 0
                    app_id = asset_queue_dict["app_id"]
                    act_id = asset_queue_dict["act_id"]
                    open_id = asset_queue_dict["open_id"]
                    user_nick = asset_queue_dict["user_nick"]
                    user_id = asset_queue_dict["user_id"]
                    asset_type = asset_queue_dict["asset_type"]
                    asset_object_id = asset_queue_dict["asset_object_id"]
                    now_day_int = asset_queue_dict["now_day_int"]
                    create_date = asset_queue_dict["create_date"]
                    now_value = asset_queue_dict["now_value"]
                    operate_value = asset_queue_dict["operate_value"]
                    history_asset_value = asset_queue_dict["history_asset_value"]
                    asset_inventory_id_md5 = CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}_{asset_type}_{asset_object_id}_{now_day_int}")
                    asset_inventory = asset_inventory_model.get_cache_entity("id_md5=%s",params=[asset_inventory_id_md5])
                    asset_inventory_update_sql = f"process_count=0,now_value={now_value}"
                    if asset_inventory:
                        old_asset_inventory_id = asset_inventory.id
                        if operate_value > 0:
                            asset_inventory_update_sql += f",inc_value=inc_value+{operate_value}"
                        else:
                            asset_inventory_update_sql += f",dec_value=dec_value+{operate_value}"
                    else:
                        asset_inventory = AssetInventory()
                        asset_inventory.id_md5 = asset_inventory_id_md5
                        asset_inventory.app_id = app_id
                        asset_inventory.act_id = act_id
                        asset_inventory.user_id = user_id
                        asset_inventory.open_id = open_id
                        asset_inventory.user_nick = user_nick
                        asset_inventory.asset_type = asset_type
                        asset_inventory.asset_object_id = asset_object_id
                        if operate_value > 0:
                            asset_inventory.inc_value += operate_value
                        else:
                            asset_inventory.dec_value += operate_value
                        asset_inventory.history_value = history_asset_value
                        asset_inventory.now_value = now_value
                        asset_inventory.create_date = create_date
                        asset_inventory.create_day = now_day_int
                    if old_asset_inventory_id != 0:
                        asset_inventory_model.update_table(asset_inventory_update_sql, "id=%s", params=[old_asset_inventory_id])
                    else:
                        asset_inventory_model.add_entity(asset_inventory)
                except Exception as ex:
                    asset_queue_dict["process_count"] += 1
                    if asset_queue_dict["process_count"] <= 10:
                        redis_init.rpush(f"asset_queue_list", SevenHelper.json_dumps(asset_queue_dict))
                    else:
                        logger_error.error(f"资产队列异常,json串:{SevenHelper.json_dumps(asset_queue_dict)},ex:{traceback.format_exc()}")
                    continue
            except Exception as ex:
                logger_error.error(f"资产队列异常,ex:{traceback.format_exc()}")
                time.sleep(5)

    def _process_asset_intercept_queue(self):
        """
        :description: 处理资产拦截队列入库
        :return: 
        :last_editors: HuangJianYi
        """
        while True:
            try:
                time.sleep(0.1)
                redis_init = SevenHelper.redis_init()
                asset_warn_notice_model = AssetWarnNoticeModel()
                queue_json = redis_init.lpop(f"asset_intercept_queue_list")
                if not queue_json:
                    time.sleep(1)
                    continue
                try:
                    queue_dict = SevenHelper.json_loads(queue_json)
                    asset_warn_notice = SevenHelper.auto_mapper(AssetWarnNotice,queue_dict)
                    asset_warn_notice_model.add_entity(asset_warn_notice)
                except Exception as ex:
                    continue
            except Exception as ex:
                logger_error.error(f"资产拦截队列异常,ex:{traceback.format_exc()}")
                time.sleep(5)