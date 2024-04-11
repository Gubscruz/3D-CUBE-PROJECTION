from variaveis import *
import pygame
import numpy as np

class Cube:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('APS4 ALG LIN')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.d = 1  # distancia focal
        self.angles = (0, 0, 0) # angulos de rotacao
        self.x_offset = 0 # translacao no eixo x (movimetacao lateral)
        # matriz de projeção
        self.P = np.array([ [1, 0, 0,      0   ],
                            [0, 1, 0,      0   ],
                            [0, 0, 0,   -self.d],
                            [0, 0, -1/self.d, 0] ])
        # matriz de escala
        self.S = np.array([ [-WIDTH//2, 0, 0],
                            [0, HEIGHT//2, 0],
                            [0, 0, 1] ])
        # matriz de translação
        self.T = np.array([ [1, 0, WIDTH//2],
                            [0, 1, HEIGHT//2],
                            [0, 0, 1] ])

        cube = np.array([[1, 1, 1],
                         [1, 1, -1],
                         [1, -1, 1],
                         [1, -1, -1],
                         [-1, 1, 1],
                         [-1, 1, -1],
                         [-1, -1, 1],
                         [-1, -1, -1]]).T
        # cada coluna eh um ponto (x, y, z, 1) (coordenadas homogeneas)
        self.cube = np.vstack((cube, np.ones(cube.shape[1])))


    def rotate_cube(self, angles: tuple) -> np.array: 
        angle_x, angle_y, angle_z = angles
        angle_x = np.radians(angle_x)
        angle_y = np.radians(angle_y)
        angle_z = np.radians(angle_z)

        Rx = np.array([[1, 0, 0, 0],
                       [0, np.cos(angle_x), -np.sin(angle_x), 0],
                       [0, np.sin(angle_x), np.cos(angle_x), 0],
                       [0, 0, 0, 1]])
        Ry = np.array([[np.cos(angle_y), 0, np.sin(angle_y), 0],
                       [0, 1, 0, 0],
                       [-np.sin(angle_y), 0, np.cos(angle_y), 0],
                       [0, 0, 0, 1]])
        Rz = np.array([[np.cos(angle_z), -np.sin(angle_z), 0, 0],
                       [np.sin(angle_z), np.cos(angle_z), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        
        rotated_cube = Rz @ Ry @ Rx @ self.cube
        # transalcao no eixo z (para o cubo nao ficar edm cima do pin hole - que esta no eixo z = 0)
        rotated_cube[2] = rotated_cube[2] + 4
        rotated_cube[0] += self.x_offset

        return rotated_cube


    def draw_cube(self, points: np.array) -> None:
        edges = [(0, 1), (1, 3), (3, 2), (2, 0),
                 (4, 5), (5, 7), (7, 6), (6, 4),
                 (0, 4), (1, 5), (3, 7), (2, 6)]
        for edge in edges:
            pygame.draw.circle(self.screen, WHITE, (int(points[edge[0]][0]), int(points[edge[0]][1])), 5)
            pygame.draw.line(self.screen, RED, points[edge[0]], points[edge[1]], 2)


    def project(self, points: np.array) -> np.array:
        # aplica a matriz de projeção
        projection = self.P @ points
        # (xw, yw, z, w) -> (x, y, z/w), normaliza as coordenadas
        projection = projection / projection[3]

        # pega coordenadas x e y (z é descartado) e transforma em coordenadas homogeneas (x, y, 1)
        poins_2d = projection[:2]
        poins_2d = np.vstack((poins_2d, np.ones(poins_2d.shape[1])))

        # aplica a matriz de escala
        scaled = self.S @ poins_2d
        # aplica a matriz de translação para o centro da tela
        projection = self.T @ scaled

        return projection[:2].T

    def update_P(self):
        self.P[2, 3] = -self.d
        self.P[3, 2] = -1/self.d


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys = pygame.key.get_pressed()

            # translada o cubo no eixo x de acordo com o movivemto
            if keys[pygame.K_a]:
                self.x_offset += 0.069
            if keys[pygame.K_d]:
                self.x_offset -= 0.069

            # muda a distancia focal de acordo com o movimento
            if keys[pygame.K_w]:
                self.d += 0.0169
                self.update_P()
            if keys[pygame.K_s]:
                self.d -= 0.0169
                self.update_P()

            self.screen.fill(BLACK)

            self.angles = (self.angles[0] + 1, self.angles[1] + 1, self.angles[2] + 1)
            rotated_cube = self.rotate_cube(self.angles)
            projected_cube = self.project(rotated_cube)
            self.draw_cube(projected_cube)

            pygame.display.flip()
            self.clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    cube = Cube()
    cube.run()