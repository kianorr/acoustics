import numpy as np
import math

class NecessaryEquations:
    def __init__(self):
        pass

    def get_angular_frequency(self, frequency):
        return 2 * np.pi * frequency

    def get_power(self, sound_level_decibels, radius):
        power = 4 * np.pi * radius**2 * 10**-12 * 10**(sound_level_decibels / 10)
        return power

    def get_tot_amplitude_sqrt(self, power, air_density, sound_speed_meters, angular_frequency, sound_absorption_val, sound_absorption=True):

        total_amplitude_sqrt = math.sqrt(power / (2 * np.pi * air_density * sound_speed_meters * angular_frequency**2)) #Amplitude of sound wave
        total_amplitude_absorbed_sqrt = math.sqrt(power * sound_absorption_val / (2 * np.pi * air_density * sound_speed_meters * angular_frequency**2)) #Amplitude of absorbed sound wave

        if sound_absorption == True:
            return total_amplitude_absorbed_sqrt
        else:
            return total_amplitude_sqrt


class PathInfo:

    def __init__(self, angular_frequency, time):
        self.angular_frequency = angular_frequency
        self.time = time
        pass

    #path going directly to coordinate (all of the geometry was done on paper and is on Github)
    def get_direct_path(self, x_coord, y_coord):
        '''Path that goes directly to current coordniate.'''
        direct_path = math.sqrt(x_coord**2 + y_coord**2)
        return direct_path

    #paths going from the source to the wall
    def get_lower_paths(self, x_coord, y_coord, mid_distance):
        lower_path = mid_distance * math.sqrt(y_coord / (2 * mid_distance + x_coord)**2 + 1)
        return lower_path

    #paths going from wall to source
    def get_upper_paths(self, x_coord, y_coord, mid_distance):
        upper_path = math.sqrt((y_coord * (2 * mid_distance + x_coord / mid_distance))**2 + (mid_distance + y_coord)**2)
        return upper_path

    #differences between paths
    def get_path_difference(self, lower_path, upper_path, direct_path):
        path_difference = lower_path + upper_path - direct_path
        return path_difference

    #phase difference
    def get_phase_difference(self, path, frequency, sound_speed_meters):
        phase_difference = 2 * np.pi * path * frequency / sound_speed_meters
        return phase_difference

    #total amplitude
    def get_total_amplitude(self, amplitude_type, lower_path, upper_path):
        total_amplitude = amplitude_type / (lower_path + upper_path)
        return total_amplitude

    #x component of amplitude
    def get_x_amplitude(self, total_amplitude, phase_difference):
        amplitude_x = total_amplitude * np.cos(self.angular_frequency * self.time + phase_difference)
        return amplitude_x

    #y component of amplitude
    def get_y_amplitude(self, total_amplitude, phase_difference):
        amplitude_y = total_amplitude * np.sin(self.angular_frequency * self.time + phase_difference)
        return amplitude_y