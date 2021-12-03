import numpy as np
import env
from env import buildEnvironment
import sensors
import features
import pygame
import random
def random_color():
    levels = range(32, 256, 32)
    return tuple(random.choice(levels)for _ in range(3))
FeatureMap = features.featuresDetection()
environment = buildEnvironment((600,1200))
originalMap = environment.map.copy()
laser = sensors.LaserSensor(200, originalMap, uncertainity=(0.5,0.01))
environment.map.fill((255,255,255))
environment.infomap = environment.map.copy()
originalMap = environment.map.copy()
running = True
FEATURE_DETECTION = True
BREAK_POINT_IND = 0

while running:
    environment.infomap = originalMap.copy()
    FEATURE_DETECTION = True
    BREAK_POINT_IND = 0
    ENDPOINTS = [0, 0]
    sensorON = False
    PREDICTED_POINTS_TODRAW = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_focused():
        sensorON = True
    elif not pygame.mouse.get_focused():
        sensorON = False
    if sensorON:
        position = pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles()
        FeatureMap.laser_points_set(sensor_data)
        while BREAK_POINT_IND <(FeatureMap.NP - FeatureMap.PMIN):
            seedseg = FeatureMap.seed_segment_detection(laser.position, BREAK_POINT_IND)
            if seedseg == False:
                break
            else:
                seedSegment = seedseg[0]
                PREDICTED_POINTS_TODRAW = seedseg[1]
                INDICES = seedseg[2]
                results = FeatureMap.seed_segment_growing(INDICES, BREAK_POINT_IND)
                if results == False:
                    BREAK_POINT_IND = INDICES[1]
                    continue
                else:

                    line_eq = results[1]
                    m, c = results[5]
                    line_seg = results[0]
                    OUTERMOST = results[2]
                    BREAK_POINT_IND = results[3]

                    ENDPOINTS[0] = FeatureMap.projection_point2line(OUTERMOST[0], m, c)
                    ENDPOINTS[1] = FeatureMap.projection_point2line(OUTERMOST[1], m, c)

                    COLOR = random_color()
                    for point in line_seg:
                        environment.infomap.set_at((int(point[0][0]), int(point[0][1])),(0,255,0))
                        pygame.draw.circle(environment.infomap, COLOR, (int(point[0][0]), int(point[0][1])),2,0)
                    pygame.draw.line(environment.infomap, (255, 0 , 0), ENDPOINTS[0], ENDPOINTS[1], 2)

                    environment.dataStorage(sensor_data)
    environment.map.blit(environment.infomap, (0,0))
    pygame.display.update()