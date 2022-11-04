from enum import Enum
import os


class Paths(Enum):
    ROOT_DIR = os.path.abspath(os.curdir)
    BACKUP_DIR = os.path.join(ROOT_DIR, 'Backup')
    ERROR_DIR = os.path.join(ROOT_DIR, 'Error')
    INVENTORY_DIR = os.path.join(ROOT_DIR, 'InventoryList.txt')
    NOT_AUT_BACKUP_DIR = os.path.join(ROOT_DIR.value, 'Not_Aut_Backup')
    NOT_REACH_BACKUP_DIR = os.path.join(ROOT_DIR.value, 'Not_Reach_Backup')
    SSH_FAILURE_DIR = os.path.join(ROOT_DIR.value, 'SSH_Failure')

    @classmethod
    def ROOT_PATH(cls):
        return cls.ROOT_DIR.value

    @classmethod
    def BACKUP_PATH(cls):
        return cls.BACKUP_DIR.value

    @classmethod
    def ERROR_PATH(cls):
        return cls.ERROR_DIR.value

    @classmethod
    def INVENTORY_PATH(cls):
        return cls.INVENTORY_DIR.value

    @classmethod
    def NOT_AUT_BACKUP_PATH(cls):
        return cls.NOT_AUT_BACKUP_DIR.value

    @classmethod
    def NOT_REACH_BACKUP_PATH(cls):
        return cls.NOT_REACH_BACKUP_DIR.value

    @classmethod
    def SSH_FAILURE_PATH(cls):
        return cls.SSH_FAILURE_DIR.value
