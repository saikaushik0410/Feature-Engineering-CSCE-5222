import math 
import pygame
class buildEnvironment:
    def __init__(self,MapDimensions):
        pygame.init()
        self.PointCloud = []
        self.externalMap = pygame.image.load('floor.png')
        self.maph, self.mapw = MapDimensions
        self.MapWindowName = 'Lidar point cloud'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.externalMap,(0,0))
        ## colors 
        self.black = (0,0,0)
        self.grey = (70,70,70)
        self.blue = (0,0,255)
        self.green = (0,255,0)
        self.red = (255,0,0)
        self.white=(255,255,255)
    
    def AD2pos(self, distance, angle, robotposition):
        x = distance *math.cos(angle) + robotposition[0]
        y = -distance * math.sin(angle) + robotposition[1]

        return (int(x), int(y))

    def dataStorage(self, data):
        print(len(self.PointCloud))
        for element in data:
            point = self.AD2pos(element[0], element[1], element[2])
            if point not in self.PointCloud:
                self.PointCloud.append(point)

    def show_sensorData(self):
        self.infomap = self.map.copy()
        for point in self.PointCloud:
            self.infomap.set_at((int(point[0]), int(point[1])), (255,0,0))
            