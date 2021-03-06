# -*- coding:utf-8 -*-
'''
基于PCA9685 I2C舵机控制模块对舵机进行控制的库

上臂舵机 控制精度: 0.45度
下臂舵机 控制精度: 0.63度
'''
import pca9685
import math
from car_config import car_property

class Servo:
    '''
    利用PCA9685控制Servo
    '''
    def __init__(self, pca9685, servo_idx, min_duty=30, max_duty=130, angle_range=180, default_angle=90):
        '''
        Servo的构造器
        '''
        # PCA9685舵机驱动板
        self.pca9685 = pca9685
        # 舵机在PCA9695舵机驱动板上的编号
        self.servo_idx = servo_idx
        # 舵机最小角度时候的占空比
        self.min_duty = min_duty
        # 舵机最大角度时候的占空比
        self.max_duty = max_duty
        # 舵机角度范围
        self.angle_range = angle_range
        # 舵机默认角度
        self.default_angle = default_angle
        # 当前的角度值
        self._angle = default_angle
        # 舵机旋转到默认的角度
        self.angle(default_angle)
        

    def _angle2duty(self, angle):
        duty = self.min_duty + (self.max_duty - self.min_duty)*( angle / self.angle_range)
        return int(duty)

    def angle(self, value=None):
        if value is None:
            # 返回当前舵机的角度
            return self._angle
        else:
            value = float(value)
            # 计算舵机的占空比
            duty = self._angle2duty(value)
            # 执行指令
            self.pca9685.duty(self.servo_idx, duty)
            # 更新当前的角度值
            self._angle = value
    
    def reset(self):
        self.angle(self.default_angle)

class CloudPlatform:
    '''
    舵机云台
    PCA9685的Duty取值范围为 0- 4095
    '''
    def __init__(self, i2c, address=0x40, freq=50):
        # 创建PCA9685对象
        self.pca9685 = pca9685.PCA9685(i2c, address)
        # 设定PWM的频率
        self.pca9685.freq(freq)

        self.bottom_servo = Servo(
            self.pca9685,
            car_property['BOTTOM_SERVO_IDX'],
            min_duty=car_property['BOTTOM_SERVO_MIN_DUTY'],
            max_duty=car_property['BOTTOM_SERVO_MAX_DUTY'],
            angle_range=car_property['BOTTOM_SERVO_ANGLE_RANGE'],
            default_angle=car_property['BOTTOM_SERVO_DEFAULT_ANGLE'])
        
        self.top_servo = Servo(
            self.pca9685,
            car_property['TOP_SERVO_IDX'],
            min_duty=car_property['TOP_SERVO_MIN_DUTY'],
            max_duty=car_property['TOP_SERVO_MAX_DUTY'],
            angle_range=car_property['TOP_SERVO_ANGLE_RANGE'],
            default_angle=car_property['TOP_SERVO_DEFAULT_ANGLE'])
    
    def down(self, delta_angle=5):
        '''
        云台上臂向下
        '''
        delta_angle = float(delta_angle)

        cur_angle = self.top_servo.angle()
        target_angle = cur_angle - delta_angle

        if target_angle >= 0:
            self.top_servo.angle(target_angle)
    
    def up(self, delta_angle=5):
        '''
        云台上臂向上
        '''
        delta_angle = float(delta_angle)

        cur_angle = self.top_servo.angle()
        target_angle = cur_angle + delta_angle

        if target_angle <= self.top_servo.angle_range:
            self.top_servo.angle(target_angle)
    
    def left(self, delta_angle=5):
        '''
        云台下臂向左
        '''
        delta_angle = float(delta_angle)

        cur_angle = self.bottom_servo.angle()
        target_angle = cur_angle + delta_angle

        if target_angle <= self.bottom_servo.angle_range:
            self.bottom_servo.angle(target_angle)
            
    def right(self, delta_angle=5):
        '''
        云台下臂向右
        '''
        delta_angle = float(delta_angle)
        
        cur_angle = self.bottom_servo.angle()
        target_angle = cur_angle - delta_angle

        if target_angle >= 0:
            self.bottom_servo.angle(target_angle)
    
    def reset(self):
        
        self.top_servo.reset()
        self.bottom_servo.reset()

if __name__ == '__main__':
    '''
    测试舵机云台
    '''
    from machine import I2C,Pin
    from car_config import gpio_dict, car_property
    # from cloud_platform import CloudPlatform

    # 创建一个I2C对象
    i2c = I2C(
        scl=Pin(gpio_dict['I2C_SCL']),
        sda=Pin(gpio_dict['I2C_SDA']),
        freq=car_property['I2C_FREQUENCY'])

    # 创建云台对象
    cp = CloudPlatform(i2c)
