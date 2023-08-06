
##LYRA MODULE

from pymodbus.client.sync import ModbusSerialClient
from pymodbus import payload
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
from pymodbus.utilities import computeCRC
import numpy as np
import time

def reset_Lyra(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0002)
        builder.add_16bit_uint(0x0001)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        return
    except:
        raise

def Lyra_factory_reset(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0002)
        builder.add_16bit_uint(0x0002)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        return
    except:
        raise


def read_time_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=5004,count=2,unit=target_unit)
        if not request.isError():
            time=int(str(request.registers[0])+str(request.registers[1]))
            #print('Time from unit ',target_unit," is ",time)
            return time
    except:
        raise
    

def read_k1_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=5000,count=2,unit=target_unit)
        if not request.isError():
            return hex(request.registers[0]),hex(request.registers[1])
    except:
        raise

def read_system_status(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=5016,count=2,unit=target_unit)
        if not request.isError():
            return hex(request.registers[0]),hex(request.registers[1])
    except:
        raise

def reset_time_register(client,target_unit,time_to_write):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=5004,values=[0x0000,time_to_write],unit=target_unit)
        request=client.read_holding_registers(address=5004,count=2,unit=target_unit)
        if not request.isError():
            time=int(str(request.registers[0])+str(request.registers[1]))
            print('Time from unit ',target_unit," is ",time)
            return time
    except:
        raise

def change_id_register_to_default(client,target_unit):
    #ID is composed by two 16-bit digits.
    new_id=2
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x5A5A)
        builder.add_16bit_uint(new_id)
        payload = builder.build()
        result  = client.write_registers(5200, payload, skip_encode=True)
        return
        # rq=client.write_registers(5200,[0x0000],unit=target_unit)
        # rq=client.write_registers(5201,[new_id],unit=target_unit)
    except:
        raise
def change_bt_timeout(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_32bit_float(new_value)
        payload = builder.build()
        result  = client.write_registers(7220, payload, skip_encode=True)
        return
        # rq=client.write_registers(5200,[0x0000],unit=target_unit)
        # rq=client.write_registers(5201,[new_id],unit=target_unit)
    except:
        raise 

def change_btconfig_parameters(client,target_unit,values):
    #ID is composed by two 16-bit digits.
    for i in range(14):
        value_to_write=values[i]
##        print(value_to_write,7220+2*i)
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_float(value_to_write)
            payload = builder.build()
            result  = client.write_registers(7200+2*i, payload, skip_encode=True)
            time.sleep(0.1)
            print('Value ',value_to_write,' successfully written at register: ',7200+2*i)
            # rq=client.write_registers(5200,[0x0000],unit=target_unit)
            # rq=client.write_registers(5201,[new_id],unit=target_unit)
        except:
            raise
    print('All values succesfully written')
    return

def change_guconfig_parameters(client,target_unit,values):
    #ID is composed by two 16-bit digits.
    for i in range(7):
        value_to_write=values[i]
##        print(value_to_write,7220+2*i)
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_float(value_to_write)
            payload = builder.build()
            result  = client.write_registers(7228+2*i, payload, skip_encode=True)
            time.sleep(0.1)
            print('Value ',value_to_write,' successfully written at register: ',7228+2*i)
            # rq=client.write_registers(5200,[0x0000],unit=target_unit)
            # rq=client.write_registers(5201,[new_id],unit=target_unit)
        except:
            raise
    print('All values succesfully written')
    return

def change_sbconfig_parameters(client,target_unit,values):
    #ID is composed by two 16-bit digits.
    for i in range(11):
        value_to_write=values[i]
##        print(value_to_write,7220+2*i)
        try:
            builder = BinaryPayloadBuilder(byteorder=Endian.Big)
            builder.add_32bit_float(value_to_write)
            payload = builder.build()
            result  = client.write_registers(7242+2*i, payload, skip_encode=True)
            time.sleep(0.1)
            print('Value ',value_to_write,' successfully written at register: ',7242+2*i)
            # rq=client.write_registers(5200,[0x0000],unit=target_unit)
            # rq=client.write_registers(5201,[new_id],unit=target_unit)
        except:
            raise
    print('All values successfully written')
    return
            
def change_id_register(client,target_unit,target_id):
    #ID is composed by two 16-bit digits.
    new_id=target_id
    try:
        rq=client.write_registers(5200,[0x5A5A,new_id],unit=target_unit)
        print('ID of unit ',target_unit,' has been changed successfully to ',target_id)
        return
        # rq=client.write_registers(5201,,unit=target_unit)
    except:
        raise   
        
def broadcast_default_ID(client):
    try:
        rq=client.write_registers(5200,[0x5A5A,1],unit=0)
        return
    except:
        raise
        
def broadcast_get_IDs(client):
    #This needs to be improved to associate the response with the incoming ID.
    try:
        print('Trying to get IDs from the network via broadcasting to unit 0...')
        rq=client.read_holding_registers(5200,count=2,unit=0)
        if not rq.isError():
            print('IDs from network gathered successfully...')
        return rq
    except:
        print('Unable to retrieve network devices IDs')
        return client.read_holding_registers(5200,count=2,unit=0)
        raise

def broadcast_reset_Lyra(client):
    try:
        rq=client.write_registers(5000,[0x0002],unit=0)
        rq=client.write_registers(5001,[0x0001],unit=0)
    except:
        raise
        
def K1_contactor_sync(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0010)
        builder.add_16bit_uint(0x0001)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Sync attempt of K1 at: ',str(dt.datetime.now()))
        return
    except:
        raise
        
def K1_contactor_forced_closing(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0010)
        builder.add_16bit_uint(0x0002)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Forced close of K1 at',str(dt.datetime.now()))
        return
    except: 
        raise

def K1_contactor_forced_opening(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0010)
        builder.add_16bit_uint(0x0003)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Forced opening of K1 at',str(dt.datetime.now()))
        return
    except: 
        raise

def K2_contactor_sync(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0020)
        builder.add_16bit_uint(0x0001)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Sync attempt of K2 at: ',str(dt.datetime.now()))
        return
    except: 
        raise
        
def K2_contactor_forced_closing(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0020)
        builder.add_16bit_uint(0x0002)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Forced close of K2 at',str(dt.datetime.now()))
        #rq = client.write_registers(5001, [0x0002], unit=target_unit)
        return
    except: 
        raise

def K2_contactor_forced_opening(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0020)
        builder.add_16bit_uint(0x0003)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Forced opening of K2 at',str(dt.datetime.now()))
        return
    except: 
        raise

def K1_contactor_donothing(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0000)
        builder.add_16bit_uint(0x0000)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Registers 5000 with "do nothing" cmd at: ',str(dt.datetime.now()))
        return
    except: 
        raise


def K2_contactor_donothing(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0000)
        builder.add_16bit_uint(0x0000)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Registers 5000 with "do nothing" cmd at: ',str(dt.datetime.now()))
        return
    except: 
        raise



def K3_contactor_donothing(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0000)
        builder.add_16bit_uint(0x0000)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Registers 5000 with "do nothing" cmd at: ',str(dt.datetime.now()))
        return
    except: 
        raise

def K3_contactor_sync(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0030)
        builder.add_16bit_uint(0x0001)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Sync attempt of K3 at: ',str(dt.datetime.now()))
        return
    except: 
        raise
        
def K3_contactor_forced_closing(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0030)
        builder.add_16bit_uint(0x0002)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Forced close of K3 at',str(dt.datetime.now()))
        return
    except: 
        raise

def K3_contactor_forced_opening(client,target_unit):
    try:
        builder = BinaryPayloadBuilder(byteorder=Endian.Big)
        builder.add_16bit_uint(0x0030)
        builder.add_16bit_uint(0x0003)
        payload = builder.build()
        result  = client.write_registers(5000, payload, skip_encode=True)
        print('Forced opening of K3 at',str(dt.datetime.now()))
        return
    except: 
        raise

#Reading purpose functions
###
### Functions:
#read_min_volt_conn_register(client,1)
#read_max_volt_conn_register(client,1)

#read_min_volt_disc_register(client,1)
#read_max_volt_disc_register(client,1)

#read_max_volt_diff_disc_register(client,1)
#read_max_volt_diff_conn_register(client,1)

#read_max_freq_diff_conn_register(client,1)

#read_max_angle_diff_conn_register(client,1)
#read_max_angle_diff_disc_register(client,1)

#read_conn_timeout_register(client,1)
def read_k1_status(client,target_unit):
    try:
        rq=client.read_coils(1000,unit=target_unit)
        return rq.bits[0]
    except:
        raise

def read_flags(client,target_unit):
    try:
        values=[]
        for i in range(0,3):
            request=client.read_holding_registers(address=5010+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
            c,d='{0:016b}'.format(client.read_holding_registers(address=5010,count=2,unit=8).registers[0]),'{0:016b}'.format(client.read_holding_registers(address=5010,count=2,unit=8).registers[1])
            if not request.isError():                
                value=decoder.decode_32bit_uint()
##                values.append(['{0:032b}'.format(value),c,d])
                values.append('{0:032b}'.format(value))
        return values
    except:
        raise


def read_config_parameters(client,target_unit,app):
    if app=='bt':
        #ID is composed by two 16-bit digits.
        try:
            values=[]
            for i in range(0,14):
                request=client.read_holding_registers(address=7200+i*2,count=2,unit=target_unit)
                decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
                if not request.isError():
                    value=decoder.decode_32bit_float()
                    values.append(value)
            return values
        except:
            raise

    if app=='gu':
        #ID is composed by two 16-bit digits.
        try:
            values=[]
            for i in range(7):
                request=client.read_holding_registers(address=7228+i*2,count=2,unit=target_unit)
                decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
                if not request.isError():
                    value=decoder.decode_32bit_float()
                    values.append(value)
            return values
        except:
            raise
        
    if app=='sb':
        #ID is composed by two 16-bit digits.
        try:
            values=[]
            for i in range(0,11):
                request=client.read_holding_registers(address=7242+i*2,count=2,unit=target_unit)
                decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
                if not request.isError():
                    value=decoder.decode_32bit_float()
                    values.append(value)
            return values
        except:
            raise


def read_id_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=5200,count=2,unit=target_unit)
        if not request.isError():
            print('ID from unit ',target_unit," is ",request.registers)
        return request.registers
    except:
        raise


def read_min_volt_conn_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7204,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Min voltage for connection from unit ',target_unit," is ",value)
        return value

    except:
        raise

def read_max_volt_conn_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7206,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max voltage for connection from unit ',target_unit," is ",value)
        return value

    except:
        raise
        

def read_min_volt_disc_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7214,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Min voltage for disconnection from unit ',target_unit," is ",value)
        return value

    except:
        raise

def read_max_volt_disc_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7216,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max voltage for disconnection from unit ',target_unit," is ",value)
        return value

    except:
        raise

def read_max_volt_diff_disc_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7218,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max voltage difference for disconnection from unit ',target_unit," is ",value)
        return value

    except:
        raise

def read_max_volt_diff_conn_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7210,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max voltage difference for connection from unit ',target_unit," is ",value)
        return value

    except:
        raise

def read_max_freq_diff_conn_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7208,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max frequency difference for connect from unit ',target_unit," is ",value)
        return value

    except:
        raise



def read_max_angle_diff_disc_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7212,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max angle difference for connection from unit ',target_unit," is ",value)
        return value

    except:
        raise
        
def read_max_angle_diff_conn_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7202,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Max angle tolerance from unit ',target_unit," is ",value)
        return value

    except:
        raise
        
def read_conn_timeout_register(client,target_unit):
    #ID is composed by two 16-bit digits.
    try:
        request=client.read_holding_registers(address=7220,count=2,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(request.registers, byteorder=">", wordorder=">")
        if not request.isError():
            value=decoder.decode_32bit_float()
            print('Timeout value for connection from unit ',target_unit," is ",value)
        return value

    except:
        raise
        


#Phase Reading functions
#Phase Reading functions
#Phase Reading functions

def read_side_1_info(client,target_unit):
    try:
        
        result=client.read_input_registers(address=7000,count=36,unit=target_unit)
        decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
        data=[]
        for i in range(int(36/2)):
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        raise
        
def read_phase_1_info_side_1(client,target_unit):
    try:
        data=[]
        for i in range(6):
            result=client.read_input_registers(address=7000+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        raise

def read_phase_2_info_side_1(client,target_unit):
    try:
        data=[]
        for i in range(6):
            result=client.read_input_registers(address=7012+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        raise
    
def read_phase_3_info_side_1(client,target_unit):
    try:
        data=[]
        for i in range(6):
            result=client.read_input_registers(address=7024+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        raise
    
def read_phase_1_info_side_2(client,target_unit):
    try:
        data=[]
        for i in range(6):
            result=client.read_input_registers(address=7036+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        return result

def read_phase_2_info_side_2(client,target_unit):
    try:
        data=[]
        for i in range(6):
            result=client.read_input_registers(address=7048+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        raise
    
def read_phase_3_info_side_2(client,target_unit):
    try:
        data=[]
        for i in range(6):
            result=client.read_input_registers(address=7060+i*2,count=2,unit=target_unit)
            decoder = payload.BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=">", wordorder=">")
            data.append(decoder.decode_32bit_float())
        return data
    except Exception as e:
        raise
        
#Writing registers purpose functions
###
###
def write_max_angle_diff_conn_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        builder=BinaryPayloadBuilder()
        builder.add_16bit_float(new_value)
        payload=builder.build()
        print(payload)
        #wrequest=client.write_registers(address=7202,values=[new_value,0],unit=target_unit)
        wrequest=client.write_registers(address=7202,values=payload,skip_encode=True,unit=target_unit)
        if not wrequest.isError():
            print('Max angle tolerance from unit ',target_unit," now is ",new_value)
        return new_value

    except Exception as e:
        print(e)
        raise
  
def write_min_vol_conn_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7204,values=[new_value],unit=target_unit)
        if not wrequest.isError():
            print('Min voltage  connection tolerance from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise

def write_max_vol_conn_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7206,values=[new_value],unit=target_unit)
        if not wrequest.isError():
            print('Max voltage connection tolerance from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise


def write_max_freq_diff_conn_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7208,values=[0x0028],unit=target_unit)
        if not wrequest.isError():
            print('Max angle tolerance from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise

def write_max_volt_diff_conn_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7210,values=[0x0028],unit=target_unit)
        if not wrequest.isError():
            print('Max voltage difference tolerance from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise
  
def write_max_agl_diff_disc_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7212,values=[],unit=target_unit)
        if not wrequest.isError():
            print('Max angle disconnection tolerance from unit ',target_unit," now is ")
        return new_value

    except:
        raise
        
def write_min_vol_disc_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7214,values=[0x0028],unit=target_unit)
        if not wrequest.isError():
            print('Min voltage tolerance for disconnection from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise
   
def write_max_vol_disc_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7216,values=[0x0028],unit=target_unit)
        if not wrequest.isError():
            print('Max voltage tolerance for connection from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise
        
def write_max_vol_diff_disc_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7218,values=[0x0028],unit=target_unit)
        if not wrequest.isError():
            print('Max voltage difference tolerance for disconnection from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise
 
def write_conn_timeout_register(client,target_unit,new_value):
    #ID is composed by two 16-bit digits.
    try:
        wrequest=client.write_registers(address=7220,values=[0x0028],unit=target_unit)
        if not wrequest.isError():
            print('Max angle tolerance from unit ',target_unit," now is ",new_value)
        return new_value

    except:
        raise
      




####RELAY MODULES

def create_connection(comport):
    num_retries=10
    try:
        #client=ModbusSerialClient(method='rtu',port='/dev/ttyUSB'+str(comport),stopbits=1,bytesize=8,parity='N',baudrate=115200)
        client=ModbusSerialClient(method='rtu',port='COM'+str(comport),stopbits=1,bytesize=8,parity='N',baudrate=115200)
        client.connect()
        return client
    
    except:
        i=0
        while i<=num_retries:
            try:
                client=ModbusSerialClient(method='rtu',port='/dev/ttyUSB'+str(comport),stopbits=1,bytesize=8,parity='N',baudrate=115200)
                client.connect()
                i+=1
                return client
            except:
                i+=1
                pass
        raise

def close_connection(client):
    try:
        client.close()
    except:
        raise



#IDs van desde 1 a 256 (0x01 a 0xFF), broadcast ID is 0x00    
def read_slave_id_address(client,slave_id):
    # return client.read_holding_registers(address=16384,count=1,unit=slave_id).registers
    return client.read_holding_registers(address=0x4000,count=1,unit=slave_id).registers[0]

def change_slave_id(client,slave_id,target_id):
    rq=client.write_register(address=0x4000,value=target_id,unit=slave_id)
    return

def change_slave_baudrate(client,slave_id,target_baudrate):
    #     The baud rate
    # 0x0000  : 4800
    # 0x0001  : 9600
    # 0x0002  : 19200
    # 0x0003  : 38400
    # 0x0004  : 57600
    # 0x0005  : 115200
    # 0x0006  : 128000
    # 0x0007  : 256000
    try:
        client.write_register(address=0x2000,value=target_baudrate,unit=slave_id)
        print("Baudrate was modified successfully to option: ",target_baudrate)
        return
    except:
        raise


#Status readings
def read_relays_status(client,slave_id):
    #Returns a list with bools indicating status of the relays.
    #Register=0, count=8, unit=11 to 14.
    #output -> [True, True, True, True, True, True, True, True]
#   If it fails, it will give an error.
    
    retries=10
    j=0
    while j<=retries:
        #time.sleep(0.1)
        if j!=0:
            print('Attempt: ',j+1)
        req=client.read_coils(address=0,count=8,unit=slave_id)
        if not req.isError():
            req = req.bits
            out={}
            for i in range(8):
                out.update({i:req[i]})
            if j!=0:
                print('Num_Tries: ',j+1)
            return out
        time.sleep(0.1)
        j+=1
        #{0:False,1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False}
    return req 




#Individual relay handling
def close_relay(client,slave_id,relay_to_close):
    #values for relay_to_close from 0 to 7
    status=read_relays_status(client,slave_id)
    state=status[relay_to_close]
    while state==False:
        try:
            if client.is_socket_open():
                client.write_coil(address=relay_to_close,value=1,unit=slave_id)
                time.sleep(0.1)
                state=read_relays_status(client,slave_id)[relay_to_close]
        except Exception as e:
            print(e)
            raise
    return

def open_relay(client,slave_id,relay_to_close):
    #values for relay_to_close from 0 to 7
    status=read_relays_status(client,slave_id)
    state=status[relay_to_close]
    while state==True:
        try:
            if client.is_socket_open():
                client.write_coil(address=relay_to_close,value=0,unit=slave_id)
                time.sleep(0.1)
                state=read_relays_status(client,slave_id)[relay_to_close]
        except Exception as e:
            print(e)
            raise
    return

    

#Relays group handling
#Close all relays for a 
def close_all_module_relays(client,slaves_id):
    #Grid Unifying contactor data
    grid_unifying_module=14
    grid_unifying_contactor_id=0
    try:
        for slave_id in slaves_id:
            #Slave ID that contains GUC.
            try:
                status=read_relays_status(client,slave_id)
            except:
                time.sleep(0.1)
                status=read_relays_status(client,slave_id)

            if slave_id==grid_unifying_module:
                for i in range(7,0,-1):
                    if status[i]==False and i!=grid_unifying_contactor_id:
                        close_relay(client,slave_id,i)
                    else:
                        pass
            else:
                try:
                    client.write_coil(address=0x00ff,value=1,unit=slave_id)
                    time.sleep(0.1)
                    status=read_relays_status(client,slave_id)
                    for i in range(8):
                        #if its not closed
                        if status[i]==False:
                            close_relay(client,slave_id,i)
                except:
                    raise
    except:
        raise
  


def open_all_module_relays(client,slaves_id):
    #Grid Unifying contactor data
    grid_unifying_module=14
    grid_unifying_contactor_id=0
    try:
        for slave_id in slaves_id:
            #Slave ID that contains GUC.
            try:
                status=read_relays_status(client,slave_id)
            except:
                time.sleep(0.1)
                status=read_relays_status(client,slave_id)

            if slave_id==grid_unifying_module:
                for i in range(7,0,-1):
                    if status[i]==True and i!=grid_unifying_contactor_id:
                        open_relay(client,slave_id,i)
                    else:
                        pass
            else:
                try:
                    client.write_coil(address=0x00ff,value=0,unit=slave_id)
                    time.sleep(0.1)
                    status=read_relays_status(client,slave_id)
                    for i in range(8):
                        #if its not closed
                        if status[i]==True:
                            open_relay(client,slave_id,i)
                except:
                    raise
    except:
        raise
    






####UGRID CONTROL

#list devices in terminal ls /dev/*USB*

def connect_all(client):
    modules=[11,12,13,14]
    relays=[0,1,2,3,4,5,6,7]
    for module in modules:
        for relay in relays:
            close_relay(client,module,relay)
    return

def disconnect_all(client):
    modules=[14,13,12,11]
    relays=[7,6,5,4,3,2,1,0]
    for module in modules:
        for relay in relays:
            open_relay(client,module,relay)
    return

def connect_der(client,ders_to_connect):
    #ders_to_connect takes values from 1 to 6
    #der_locations={DER:(module_id,contactor)}
    der_locations={1:(11,2),2:(12,6),3:(12,2),4:(13,2),5:(14,6),6:(14,2)}
    for der in ders_to_connect:
        module=der_locations[der][0]
        contactor=der_locations[der][1]
        close_relay(client,module,contactor)
    return
    

def disconnect_der(client,ders_to_disconnect):
    #ders_to_discconnect is a list that takes values from 1 to 6
    #der_locations={DER:(module_id,contactor)}
    der_locations={1:(11,2),2:(12,6),3:(12,2),4:(13,2),5:(14,6),6:(14,2)}
    for der in ders_to_disconnect:
        module=der_locations[der][0]
        contactor=der_locations[der][1]
        open_relay(client,module,contactor)
    return

def connect_load(client,loads_to_connect):
    #loads_to_connect takes values from 1 to 12(?)
    load_locations={1:(11,3),2:(11,1),3:(12,7),4:(12,5),5:(12,3),6:(12,1),7:(13,3),8:(13,1),9:(14,7),10:(14,5),11:(14,4)}
    for load in loads_to_connect:
        module=load_locations[load][0]
        contactor=load_locations[load][1]
        close_relay(client,module,contactor)
    return
    
def disconnect_load(client,loads_to_disconnect):
    #loads_to_connect takes values from 1 to 12(?)
    load_locations={1:(11,3),2:(11,1),3:(12,7),4:(12,5),5:(12,3),6:(12,1),7:(13,3),8:(13,1),9:(14,7),10:(14,5),11:(14,4)}
    for load in loads_to_disconnect:
        module=load_locations[load][0]
        contactor=load_locations[load][1]
        open_relay(client,module,contactor)
    return
    

def connect_all_load(client):
    load_locations={1:(11,3),2:(11,1),3:(12,7),4:(12,5),5:(12,3),6:(12,1),7:(13,3),8:(13,1),9:(14,7),10:(14,4),11:(14,4)}
    for load in load_locations.keys():
        module=load_locations[load][0]
        contactor=load_locations[load][1]
        close_relay(client,module,contactor)
    return

def disconnect_all_load(client):
    load_locations={1:(11,3),2:(11,1),3:(12,7),4:(12,5),5:(12,3),6:(12,1),7:(13,3),8:(13,1),9:(14,7),10:(14,4),11:(14,4)}
    for load in load_locations.keys():
        module=load_locations[load][0]
        contactor=load_locations[load][1]
        open_relay(client,module,contactor)
    return

def connect_all_der(client):
    der_locations={1:(11,2),2:(12,6),3:(12,2),4:(13,2),5:(14,6),6:(14,2)}
    for der in der_locations.keys():
        module=der_locations[der][0]
        contactor=der_locations[der][1]
        close_relay(client,module,contactor)
    return
    
def disconnect_all_der(client):
    der_locations={1:(11,2),2:(12,6),3:(12,2),4:(13,2),5:(14,6),6:(14,2)}
    for der in der_locations.keys():
        module=der_locations[der][0]
        contactor=der_locations[der][1]
        open_relay(client,module,contactor)
    return
