def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

CommandIds = enum('MOVE','INTERACT')
ResultIds = enum('ERROR', 'SUCCESS')
MessageIds = enum( 'TICK', 'LOAD')
