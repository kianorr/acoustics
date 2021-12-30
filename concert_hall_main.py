from concert_hall_clean import PathInfo, NecessaryEquations
import math
import matplotlib.pyplot as plt
import numpy as np

#setting up matrix (size of hall)
columns = 10
rows = 15
hall_matrix = np.zeros((rows, columns))

# Initial conditions
d = columns/2 + 0.5
x = -d
y = 0
time = 1
sound_speed_meters = 344 #speed of sound
frequency = 440 #frequency
sound_level_decibels = 76 #decibels
radius = 0.1 #radius for power equation
air_density = 1.225 #air density
sound_absorption_val = 0.1 #sound absorption, a=1 is full absorption, a=0 is no absorption

n = NecessaryEquations()

angular_frequency = n.get_angular_frequency(frequency)
power = n.get_power(sound_level_decibels, radius)
total_amplitude_sqrt = n.get_tot_amplitude_sqrt(power, 
                                                air_density, 
                                                sound_speed_meters, 
                                                angular_frequency,
                                                sound_absorption_val, 
                                                sound_absorption=False,)
total_amplitude_absorbed_sqrt = n.get_tot_amplitude_sqrt(power, 
                                                air_density, 
                                                sound_speed_meters, 
                                                angular_frequency, 
                                                sound_absorption_val)

p = PathInfo(angular_frequency, time)
for i in hall_matrix:
    y += 1
    for j in range(len(i)):
        x += 1
        
        # paths as described above in functions
        direct_path = p.get_direct_path(x, y)
        left_lower_path = p.get_lower_paths(-x, y, d)
        left_upper_path = p.get_upper_paths(-x, y, d)
        right_lower_path = p.get_lower_paths(x, y, d)
        right_upper_path = p.get_upper_paths(x, y, d)
        
        #Path differences
        left_path_difference = p.get_path_difference(left_lower_path, 
                                                        left_upper_path, 
                                                        direct_path)

        right_path_difference = p.get_path_difference(right_lower_path, 
                                                        right_upper_path, 
                                                        direct_path)

        left_phase_difference = p.get_phase_difference(left_path_difference, 
                                                        frequency, 
                                                        sound_speed_meters)

        right_phase_difference = p.get_phase_difference(right_path_difference, 
                                                        frequency, 
                                                        sound_speed_meters)
        
        #Amplitudes
        left_total_amplitude = p.get_total_amplitude(total_amplitude_sqrt, 
                                                        left_lower_path, 
                                                        left_upper_path)
                                                    
        left_total_amplitude_absorbed = p.get_total_amplitude(total_amplitude_absorbed_sqrt, 
                                                                left_lower_path, 
                                                                left_upper_path)

        # x amplitudes on the left side of the concert hall.
        left_x_amplitude_unabsorbed = p.get_x_amplitude(left_total_amplitude, 
                                                        left_phase_difference)
        left_x_amplitude_absorbed = p.get_x_amplitude(left_total_amplitude_absorbed, 
                                                        left_phase_difference)
        left_x_amplitude = left_x_amplitude_unabsorbed - left_x_amplitude_absorbed

        # y amplitudes on the left side of the concert hall.
        left_y_amplitude_unabsorbed = p.get_y_amplitude(left_total_amplitude, 
                                                        left_phase_difference)
        left_y_amplitude_absorbed = p.get_y_amplitude(left_total_amplitude_absorbed, 
                                                        left_phase_difference)
        left_y_amplitude = left_y_amplitude_unabsorbed - left_y_amplitude_absorbed
        
        right_total_amplitude = p.get_total_amplitude(total_amplitude_sqrt, right_lower_path, right_upper_path)
        right_total_amplitude_absorbed = p.get_total_amplitude(total_amplitude_absorbed_sqrt, right_lower_path, right_upper_path)

        right_x_amplitude = p.get_x_amplitude(right_total_amplitude, right_phase_difference) - p.get_x_amplitude(right_total_amplitude_absorbed, right_phase_difference)
        right_y_amplitude = p.get_y_amplitude(right_total_amplitude, right_phase_difference) - p.get_y_amplitude(right_total_amplitude_absorbed, right_phase_difference)
        
            #wave that goes directly to (x,y) coord without hitting wall
        direct_total_amplitude = p.get_total_amplitude(total_amplitude_sqrt, direct_path, 0)
        direct_x_amplitude = p.get_x_amplitude(direct_total_amplitude, 0)
        direct_y_amplitude = p.get_y_amplitude(direct_total_amplitude, 0)
        
        total_amplitude = (left_x_amplitude + right_x_amplitude + direct_x_amplitude)**2 + (left_y_amplitude + right_y_amplitude + direct_y_amplitude)**2
        
        #plugging amplitudes back into intensity
        intensity = 0.5 * air_density * sound_speed_meters * angular_frequency**2 * total_amplitude
        i[j] = 10 * math.log(intensity / 10**-12)
    x = -d

#plotting of sound distribution
fig, ax = plt.subplots()
im = ax.imshow(hall_matrix, interpolation = 'spline16', vmin = np.amin(hall_matrix), vmax = np.amax(hall_matrix), origin = 'lower')
fig.colorbar(im)
plt.title('Boston Symphony Hall, a = 0.1')
plt.show()