import paramiko
import socket
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemoteSSHChecker:
    def __init__(self, hostname: str, username: str, password: str = None, key_filename: str = None, port: int = 22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self) -> bool:
        try:
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename,
                port=self.port,
                timeout=10
            )
            return True
        except Exception as e:
            logger.error(f"Bağlantı hatası: {e}")
            return False

    def check_ssh_version(self) -> Optional[str]:
        try:
            stdin, stdout, stderr = self.client.exec_command('ssh -V')
            version = stderr.read().decode().strip()
            return version
        except Exception as e:
            logger.error(f"Versiyon kontrol hatası: {e}")
            return None

    def check_config(self) -> Dict[str, Any]:
        try:
            stdin, stdout, stderr = self.client.exec_command('cat /etc/ssh/sshd_config')
            config = stdout.read().decode()
            return self._parse_config(config)
        except Exception as e:
            logger.error(f"Konfigürasyon kontrol hatası: {e}")
            return {}

    def _parse_config(self, config: str) -> Dict[str, Any]:
        security_issues = {
            'risks': [],
            'recommendations': []
        }

        config_lines = config.split('\n')
        for line in config_lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # PermitRootLogin kontrolü
                if 'PermitRootLogin' in line and 'yes' in line.lower():
                    security_issues['risks'].append('Root girişi aktif')
                    security_issues['recommendations'].append('PermitRootLogin no olarak ayarlayın')

                # Password Authentication kontrolü
                if 'PasswordAuthentication' in line and 'yes' in line.lower():
                    security_issues['risks'].append('Parola ile giriş aktif')
                    security_issues['recommendations'].append('PasswordAuthentication no olarak ayarlayın')

                # Protocol version kontrolü
                if 'Protocol' in line and '1' in line:
                    security_issues['risks'].append('SSH Protocol 1 kullanılıyor')
                    security_issues['recommendations'].append('Sadece Protocol 2 kullanın')

        return security_issues

    def check_security(self):
        if not self.connect():
            logger.error("Sunucuya bağlanılamadı!")
            return

        logger.info(f"\n=== {self.hostname} SSH Güvenlik Raporu ===")

        # SSH versiyon kontrolü
        version = self.check_ssh_version()
        if version:
            logger.info(f"SSH Versiyon: {version}")

        # Konfigürasyon kontrolü
        config_issues = self.check_config()
        
        if config_issues.get('risks'):
            logger.warning("\nTespit Edilen Riskler:")
            for risk in config_issues['risks']:
                logger.warning(f"- {risk}")

        if config_issues.get('recommendations'):
            logger.info("\nÖneriler:")
            for rec in config_issues['recommendations']:
                logger.info(f"- {rec}")

        self.client.close()

def main():
    # Kullanım örneği
    hostname = input("Hedef sunucu IP adresi: ")
    username = input("Kullanıcı adı: ")
    password = input("Şifre: ")
    
    checker = RemoteSSHChecker(
        hostname=hostname,
        username=username,
        password=password
    )
    checker.check_security()

if __name__ == "__main__":
    main()
