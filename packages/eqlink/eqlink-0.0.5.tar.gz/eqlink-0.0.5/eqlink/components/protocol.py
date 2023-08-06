"""
公共工具，协议分析
"""
from eqlink.components.link_list import LinkList
import json
import traceback

''' 全局共享：注册中心连接列表 '''
link_list = LinkList()


def protocol_analysis(protocol, storage_path):
    """
    对协议类型进行分析和处理
    :param storage_path: 本地持久化文件路径
    :param protocol: JSON协议数据
    :return: void
    """
    if protocol['type'] == 'provider register':
        ''' Provider注册 '''
        link_list.add_provider(protocol)
        ''' Provider服务列表本地持久化存储 '''
        server_backup(storage_path)
        return {'code': '1000', 'message': '服务注册执行完成!'}
    elif protocol['type'] == 'get provider':
        ''' Consumer查询Provider服务列表 '''
        # TODO 如果服务调用失败，从服务列表中移除相应的IP，backup中保留
        print('[eqlink]', type(protocol['fail_server']))
        fail_server = protocol['fail_server']

        for item in link_list.provider_list:
            print('[eqlink]', protocol['fail_server'], item, link_list.provider_list[item]['remote'])
            remote_list = link_list.provider_list[item]['remote']
            for i in remote_list:
                for j in fail_server:
                    if i['ip'] == j['IP'] and i['port'] == j['PORT']:
                        link_list.provider_list[item]['remote'].remove(i)
        server_backup(storage_path)
        return link_list.provider_list


def server_backup(storage_path):
    try:
        f = open(storage_path, "w", encoding="utf-8")
        f.write(json.dumps(link_list.provider_list))
        link_list.provider_list_backup = link_list.provider_list.copy()
    except Exception as e:
        print(traceback.format_exc())
        print('[eqlink] 文件存储失败', e)
