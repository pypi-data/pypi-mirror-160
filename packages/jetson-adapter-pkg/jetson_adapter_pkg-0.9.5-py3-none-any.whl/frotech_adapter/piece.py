from enum import Enum
from .utils import get_crc, MODBUS_SLAVE_ADDR, PORT, BAUDRATE, Communicator
import modbus_tk.defines as cst


class PIECE_STATE(Enum):
    Unblock = 0
    Block = 1
    Unknow = 2


class PIECE_ACTION(Enum):
    BLOCK = 0
    UNBLOCK = 1
    AUTO = 2


class Piece(object):
    def __init__(self, id, port=PORT, baudrate=BAUDRATE):
        if id not in (3, 4):
            raise ValueError('id must be 3 or 4')
        self.__id = id
        self._rtu = Communicator.instance(port=port, baudrate=baudrate)
        self._master = self._rtu.master
        self.__state = self.get_piece_state()
        (self.__timeout, ) = self._master.execute(MODBUS_SLAVE_ADDR,
                                                  cst.READ_HOLDING_REGISTERS,
                                                  id, 1)

    @property
    def state(self):
        self.__state = self.get_piece_state()
        return self.__state

    def act(self, value):
        if value == PIECE_ACTION.AUTO:
            tmp = 3
        elif value == PIECE_ACTION.BLOCK:
            tmp = 1
        elif value == PIECE_ACTION.UNBLOCK:
            tmp = 2
        else:
            raise ValueError('value must be PIECE_ACTION type')
        base = (self.__id - 3) * (self.__id - 2)
        pdu = bytearray([MODBUS_SLAVE_ADDR, cst.WRITE_MULTIPLE_COILS]) + \
            bytearray([0, base, 0, 2, 1, tmp])
        cmd = pdu + get_crc(pdu)
        self._master._serial.write(cmd)

    @property
    def timeout(self):
        (self.__timeout, ) = self._master.execute(MODBUS_SLAVE_ADDR,
                                                  cst.READ_HOLDING_REGISTERS,
                                                  self.__id, 1)
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        if value < 2000 or value > 10000:
            raise ValueError('timeout must between 2000~10000')
        self.__timeout = value
        self._master.execute(MODBUS_SLAVE_ADDR,
                             cst.WRITE_SINGLE_REGISTER,
                             self.__id,
                             output_value=self.__timeout)

    def get_piece_state(self):
        # 线圈4-8位依次代表左上，左下，右上，右下的限位开关状态
        unblock, block = self._master.execute(MODBUS_SLAVE_ADDR,
                                              cst.READ_COILS, (self.__id - 3) *
                                              (self.__id - 2) + 4, 2)
        if block:
            return PIECE_STATE.Block
        if unblock:
            return PIECE_STATE.Unblock
        return PIECE_STATE.Unknow
