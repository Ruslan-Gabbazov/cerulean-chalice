

class ServerEventKind:
    INITIAL = 'initial'
    AUTHORIZE = 'authorize'
    SEND = 'send'
    REMOVE = 'remove'


class ClientEventKind:
    PING_EVENT = 'ping'
    SIGNIN_EVENT = 'signin'
    SIGNUP_EVENT = 'signup'
    AUTHORIZED_EVENT = 'authorized'
    MESSAGE_EVENT = 'message'
    DISCONNECT_EVENT = 'disconnect'
