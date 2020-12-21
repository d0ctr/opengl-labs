
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math

class Lab3:
  seconds_per_frame = 0.01
  radius = 1
  moving_speed = 0
  position = 20
  img = []
  texture = 0
  dXYZ = [1, 1, 1]
  zeroXYZ = {'x' : 0, 'y' : 0, 'z' : 0}
  ligth_pos = [20, 20, 20, 1]
  light_dspot = [0, 0, 0]
  isFalling = True
  isMoving = True
  isCollapsing = False
  isExtending = False
  currentCollapse = 0
  maxExtension = 0
  maxCollapse = 0
  collapseStep = 0
  extenseStep = 0

  def __init__(self, windoww = 800, windowh = 800):
    glutInit() # Инициализация GLUT для управления окном
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # Режимы отображения: два буфера, RGB для вывода цвета, 
    glutInitWindowSize(windoww, windowh)   # Установка высоты и ширины окна
    glutInitWindowPosition(0, 0)   # Положение окна на экране
    glutCreateWindow(b'Cube') # Название окна

    glShadeModel(GL_SMOOTH)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_BLEND)
    glEnable(GL_NORMALIZE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST) # Включаем буфер глубины
    glEnable(GL_LIGHTING) # Включаем освещение, чтобы получаить разноцветные фигуры
    glEnable(GL_LIGHT0) # Включаем источник света
    glLightfv(GL_LIGHT0, GL_POSITION, self.ligth_pos) # Помещаем источник света
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, self.light_dspot) # Направляем источник света 
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 180)
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0)
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])

    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) # Двусторонняя модель света
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1])

    glRotate(45, 0, -1, 0)
    glRotate(30 , 1, 0, -1)
    glTranslatef(0, -5, 0)
    
    glutReshapeFunc(self.resizeWindow) # Устанавливаем функцию, которая должна вызываться при изменении размеров окна
    glutDisplayFunc(self.showScreen) # Устанавливаем какая функция будет заниматься отрисовкой в окне
    glutIdleFunc(self.showScreen) # Устанавливаем какую функцию вызывать пока не будет какого-то вызова извне
    
    # glutMainLoop()  # Запускаем бесконечный цикл работы программы
  
  def mySolidSphere(self, dXYZ = [1, 1, 1], radius = 1, longs = 100, lats = 100):
    glScalef(radius, radius, radius)
    for i in range(0, lats + 1):
      lat0 = math.pi * (-0.5 + (i - 1) / float(lats))
      z0 = math.sin(lat0) * dXYZ[2]
      zr0 = math.cos(lat0) 
  
      lat1 = math.pi * (-0.5 + i /  float(lats))
      z1 = math.sin(lat1) * dXYZ[2]
      zr1 = math.cos(lat1)
  
      glBegin(GL_QUAD_STRIP)
      for j in range(0, longs + 1):
        long = 2 * math.pi * (j - 1) / float(longs)
        x = math.cos(long) * dXYZ[0]
        y = math.sin(long) * dXYZ[1]

        glNormal3f(x * zr1, y * zr1, z1)
        glVertex3f(x * zr1, y * zr1, z1)
        glNormal3f(x * zr0, y * zr0, z0)
        glVertex3f(x * zr0, y * zr0, z0)
      
      glEnd()

  def drawSphere(self, dXYZ = [1, 1, 1], translate = zeroXYZ.copy(), rotate = zeroXYZ.copy(), radius = radius):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    glTranslatef(translate['x'], translate['y'], translate['z'])
    glRotatef(-45, 0, 1, 0)
    self.mySolidSphere(dXYZ = dXYZ, radius = self.radius)
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawTorus(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 128) 
    glTranslatef(0, 0, 15) 
    glRotatef(90, 1, 0, 0) # Поворачиваем тор на 90 градусов по оси x
    glutSolidTorus(self.torusInnerRadius, self.torusOuterRadius, 100, 100) # Отрисовываем тор
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawAxis(self):
    # glPushMatrix() # Запоминаем нынешнее положение оси координат
    glBegin(GL_LINES) # Настраиваем линии для отрисовки 
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(-999, 0, 0) # От центра
    glVertex3f(999, 0, 0) # до 20 по оси x

    glMaterialfv(GL_FRONT_AND_BACK,  GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, -999, 0) # От центра
    glVertex3f(0, 999, 0) # до 20 по оси y

    glMaterialfv(GL_FRONT_AND_BACK,  GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, -999) # От центра
    glVertex3f(0, 0, 999) # до 20 по оси z
    glEnd() # Останавливаем настройку и отрисовываем
    # glPopMatrix() # Восстанавливаем положение оси координат
  
  def drawLightLine(self):
    glBegin(GL_LINES)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1])
    glVertex3f(self.ligth_pos[0], self.ligth_pos[1], self.ligth_pos[2])
    glVertex3f(self.light_dspot[0], self.light_dspot[1], self.light_dspot[2])
    glEnd()

  def drawGround(self):
    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 0.5, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 80)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(10, -0.11, 0)
    glVertex3f(0, -0.11, -10)
    glVertex3f(-10, -0.11, 0)
    glVertex3f(0, -0.11, 10)
    glEnd()
    glPopMatrix()

  def showScreen(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Удаляем все с экрана
    
    height = self.position - self.radius * self.dXYZ[1]
    
    if self.isCollapsing:
      self.currentCollapse += self.collapseStep
      if abs(self.currentCollapse - self.maxCollapse) <= 5 * self.seconds_per_frame:
        self.isCollapsing = False
        self.isExtending = True
        self.maxExtension = -self.maxCollapse
        self.extenseStep = -self.collapseStep
      else:
        self.dXYZ[0] += self.collapseStep
        self.dXYZ[1] -= self.collapseStep
        self.dXYZ[2] += self.collapseStep
      self.position = self.radius * self.dXYZ[1]

    if self.isExtending:
      self.currentCollapse += self.extenseStep
      if abs(self.currentCollapse) <= 5 * self.seconds_per_frame:
        self.isExtending = False
        self.isMoving = True
        self.moving_speed *= -1
        self.dXYZ[0] = 1
        self.dXYZ[1] = 1
        self.dXYZ[2] = 1
      else:
        self.dXYZ[0] += self.extenseStep
        self.dXYZ[1] -= self.extenseStep
        self.dXYZ[2] += self.extenseStep
      self.position = self.radius * self.dXYZ[1]

    if self.isMoving:
      self.moving_speed -= 9.8 * self.seconds_per_frame
      if height + self.moving_speed <= 0:
        self.position = self.radius * self.dXYZ[1]
        self.isMoving = False
        self.isCollapsing = True
        self.maxCollapse = (abs(self.moving_speed)) / 2
        self.collapseStep = self.maxCollapse / 4
      else:
        self.position += self.moving_speed


    translate = self.zeroXYZ.copy()
    translate['y'] = self.position
    self.drawSphere(translate = translate, dXYZ = self.dXYZ) 

    self.drawGround()
    glRotate(1, 0, 1, 0)
    glutSwapBuffers() 



  def resizeWindow(self, width, height):
    size = int((width + height) / 2) # Формируем сторону для окна
    glutReshapeWindow(size, size) # Изменяем размер окна в соответствии с новыми значениями
    glViewport(0, 0, size, size) # Устанавливаем окно, на которое проецируется изображение
    glMatrixMode(GL_PROJECTION) # Далее настриваем отображение
    glLoadIdentity() # Возвращаем марицу в состояние по-умолчанию
    glOrtho(-15, 15, -15, 15, -100, 100)  # Устанавливаем параметры для ортографической проекции
    # glFrustum(-1, 1, -1, 1, 1, 100)
    gluLookAt(0, 0, 5, # Устанавливаем положение камеры x, y, z
              0, 0, 0, # Устанавливаем смещение направления камеры
              0, 1, 0) # Устанавливаем какая ось смотри вверх
    glMatrixMode(GL_MODELVIEW)
    

  def __call__(self):
    glutMainLoop()

if __name__ == '__main__':
  Lab3().__call__()