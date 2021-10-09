
import paramiko
import logging
from common.config_util import getconfig
config = getconfig()


hostname = config.get("remote_server", "hostname")
port = config.get("remote_server", "port")
username = config.get("remote_server", "username")
password = config.get("remote_server", "password")

logger = logging.getLogger(__name__)


def exec_cmd(cmd):
    logger.info('对远程服务器执行指令%s' % cmd)
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 第一次登录的认证信息
    # 连接服务器
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    # 关闭连接
    ssh.close()
    return result