import abc


class Iannouncement(abc.ABC):
    @abc.abstractmethod
    def create_Annocement():
        pass
    @abc.abstractmethod
    def modify_Announcement():
        pass

class IMessage(abc.ABC):
    @abc.abstractmethod
    def send_Message():
        pass
    @abc.abstractmethod
    def receive_Message():
        pass

class Iauth(abc.ABC):
    @abc.abstractmethod
    def login():
        pass
    @abc.abstractmethod
    def create_auth_token():
        pass
    @abc.abstractmethod
    def get_my_messages():
        pass


