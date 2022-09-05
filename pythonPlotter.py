import pygame
pygame.init()

height = 500
width = 500

screen = pygame.display.set_mode((width, height))

lineObjs = []
x = []
y = []

#index 0 = x
#index 1 = y
class lineSeg:
    def __init__(self, p0, p1, p2, p3):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        #Rect(topX, topY, wodth, height), the top left of the screen is 0, 0
        self.rP0 = pygame.rect.Rect(p0[0]-3, p0[1]-3, 6, 6)
        self.p0Dragging = False
        self.rP1 = pygame.rect.Rect(p1[0]-3, p1[1]-3, 6, 6)
        self.p1Dragging = False
        self.rP2 = pygame.rect.Rect(p2[0]-3, p2[1]-3, 6, 6)
        self.p2Dragging = False
        self.rP3 = pygame.rect.Rect(p3[0]-3, p3[1]-3, 6, 6)
        self.p3Dragging = False

    def bezier(self, p0, p1, p2, p3):
        out = []
        t = 0
        for i in range(1, 100):
            t = i/100
            pFinal = pow(1 - t, 3) * p0 + pow(1 - t, 2) * 3 * t * p1 + (1 - t) * 3 * t * t * p2 + t * t * t * p3
            out.append(pFinal)
        return out
    
    def listGen(self):
        x = self.bezier(self.p0[0], self.p1[0], self.p2[0], self.p3[0])
        y = self.bezier(self.p0[1], self.p1[1], self.p2[1], self.p3[1])
        return x, y
    
    def update(self):
        self.p0 = [self.rP0.x + 3, self.rP0.y + 3]
        self.p1 = [self.rP1.x + 3, self.rP1.y + 3]
        self.p2 = [self.rP2.x + 3, self.rP2.y + 3]
        self.p3 = [self.rP3.x + 3, self.rP3.y + 3]

# lol
list_x_offset = 20
list_y_offset = 50
pos = [[0, 0], [300, 200], [400, 100], [70, 0]]
counter = 0
test = lineSeg(pos[0], pos[1], pos[2], pos[3])

lineObjs.append(test)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keybinds
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if(pos[1][1] <= height):
                    if(pos[2][0] < width):
                        for i in range(4):
                            pos[i][0] += list_x_offset
                        counter += list_x_offset
                        lineObjs.append(lineSeg(pos[0], pos[1], pos[2], pos[3]))
                    else:
                        for i in range(4):
                            pos[i][0] -= counter
                            pos[i][1] += list_y_offset
                        counter = 0
        #dragging stuff
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in lineObjs:
                    if i.rP0.collidepoint(event.pos):
                        i.p0Dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = i.rP0.x - mouse_x
                        offset_y = i.rP0.y - mouse_y
                    elif i.rP1.collidepoint(event.pos):
                        i.p1Dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = i.rP1.x - mouse_x
                        offset_y = i.rP1.y - mouse_y
                    elif i.rP2.collidepoint(event.pos):
                        i.p2Dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = i.rP2.x - mouse_x
                        offset_y = i.rP2.y - mouse_y
                    elif i.rP3.collidepoint(event.pos):
                        i.p3Dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = i.rP3.x - mouse_x
                        offset_y = i.rP3.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                for i in lineObjs:
                    i.p0Dragging = False
                    i.p1Dragging = False
                    i.p2Dragging = False
                    i.p3Dragging = False
        elif event.type == pygame.MOUSEMOTION:
            for i in lineObjs:
                if i.p0Dragging:
                    mouse_x, mouse_y = event.pos
                    i.rP0.x = mouse_x + offset_x
                    i.rP0.y = mouse_y + offset_y
                elif i.p1Dragging:
                    mouse_x, mouse_y = event.pos
                    i.rP1.x = mouse_x + offset_x
                    i.rP1.y = mouse_y + offset_y
                elif i.p2Dragging:
                    mouse_x, mouse_y = event.pos
                    i.rP2.x = mouse_x + offset_x
                    i.rP2.y = mouse_y + offset_y
                elif i.p3Dragging:
                    mouse_x, mouse_y = event.pos
                    i.rP3.x = mouse_x + offset_x
                    i.rP3.y = mouse_y + offset_y

        #pain
        #elif pygame.key.get_pressed() == K_SPACE:
        #    test = lineSeg()
        #    xApp, yApp = test.listGen()
        #    x.append(xApp)
        #    y.append(yApp)
        #    controlApp = [test.p0, test.p1, test.p2, test.p3]
        #    controlPoints.append(exp)

    screen.fill((0, 0, 0))

    x = []
    y = []

    for i in lineObjs:
        i.update()
        temp_x, temp_y = i.listGen()
        x.append(temp_x)
        y.append(temp_y)
    
    x1, y1 = x, y
    
    for i in lineObjs:
        pygame.draw.rect(screen, (255, 0, 0), i.rP0)
        pygame.draw.rect(screen, (255, 0, 0), i.rP1)
        pygame.draw.rect(screen, (255, 0, 0), i.rP2)
        pygame.draw.rect(screen, (255, 0, 0), i.rP3)

    for j in range(len(lineObjs)):
        for i in range(len(x[j])):
            pygame.draw.circle(screen, (255, 255, 255), [x1[j][i], y1[j][i]], 2)
    #pygame.draw.circle(screen, (255, 255, 255), )

    pygame.display.flip()

pygame.quit()