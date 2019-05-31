import smbus
import time

ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02

def bmx055():
	i2c = smbus.SMBus(1)

	x_lsb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS)
	x_msb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+1)
	y_lsb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+2)
	y_msb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+3)
	z_lsb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+4)
	z_msb = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+5)

	x_value = (x_msb * 16) + ((x_lsb & 0xF0) / 16)
	x_value = x_value if x_value < 2048 else x_value - 4096
	y_value = (y_msb * 16) + ((y_lsb & 0xF0) / 16)
	y_value = y_value if y_value < 2048 else y_value - 4096
	z_value = (y_msb * 16) + ((y_lsb & 0xF0) / 16)
	z_value = y_value if y_value < 2048 else y_value - 4096

	x_acc = x_value * 0.0098
	y_acc = y_value * 0.0098
	z_acc = z_value * 0.0098

	print("[%f, %f, %f]" % (x_acc, y_acc, z_acc))

	i2c.close()

while 1:
	bmx055()
	time.sleep(1)
