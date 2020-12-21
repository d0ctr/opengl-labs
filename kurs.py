from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math
import json

class Kurs:
  seconds_per_frame = 0.005
  
  spinning_angle = 0
  moving_angle = 0
  throtle_angle = 0
  moving_speed = 3 # m/s
  axeliration = -1
  moving_radius = 3
  cubeSide = 2
  dodecR = 0.6
  dodecX = 0
  dodecZ = dodecR

  width = 800
  height = 800
  yaw = 0
  pitch = 0

  img = []
  cubeTexture = 0
  dodecTexture = 1
  dXYZ = [1, 1, 1]
  zeroXYZ = {'x' : 0, 'y' : 0, 'z' : 0}
  ligth_pos = [20, 20, 20, 1]
  light_dspot = [0, 0, 0]

  phi = (1 + math.sqrt(5)) / 2
  c = 2 - phi
  b = 1 / phi
  
  ver = [
    [           0.0,  1.61803398875,  0.61803398875],
    [-          1.0,            1.0,            1.0],
    [-0.61803398875,            0.0,  1.61803398875],
    [ 0.61803398875,            0.0,  1.61803398875],
    [           1.0,            1.0,            1.0],
    [           0.0,  1.61803398875, -0.61803398875],
    [           1.0,            1.0, -          1.0],
    [ 0.61803398875,            0.0, -1.61803398875],
    [-0.61803398875,            0.0, -1.61803398875],
    [-          1.0,            1.0, -          1.0],
    [           0.0, -1.61803398875,  0.61803398875],
    [           1.0, -          1.0,            1.0],
    [-          1.0, -          1.0,            1.0],
    [           0.0, -1.61803398875, -0.61803398875],
    [-          1.0, -          1.0, -          1.0],
    [           1.0, -          1.0, -          1.0],
    [ 1.61803398875, -0.61803398875,            0.0],
    [ 1.61803398875,  0.61803398875,            0.0],
    [-1.61803398875,  0.61803398875,            0.0],
    [-1.61803398875, -0.61803398875,            0.0]
  ]
  normal_vectors = [
    [            0.0,  0.525731112119,  0.850650808354,],
    [            0.0,  0.525731112119, -0.850650808354,],
    [            0.0, -0.525731112119,  0.850650808354,],
    [            0.0, -0.525731112119, -0.850650808354,],

    [ 0.850650808354,             0.0,  0.525731112119,],
    [-0.850650808354,             0.0,  0.525731112119,],
    [ 0.850650808354,             0.0, -0.525731112119,],
    [-0.850650808354,             0.0, -0.525731112119,],

    [ 0.525731112119,  0.850650808354,             0.0,],
    [ 0.525731112119, -0.850650808354,             0.0,],
    [-0.525731112119,  0.850650808354,             0.0,],
    [-0.525731112119, -0.850650808354,             0.0]
  ]
  faces = [
    [ 0,  1,  2,  3,  4], 
    [ 5,  6,  7,  8,  9], 
    [10, 11,  3,  2, 12], 
    [13, 14,  8,  7, 15], 

    [ 3, 11, 16, 17,  4], 
    [ 2,  1, 18, 19, 12], 
    [ 7,  6, 17, 16, 15], 
    [ 8, 14, 19, 18,  9], 

    [17,  6,  5,  0,  4], 
    [16, 11, 10, 13, 15], 
    [18,  1,  0,  5,  9], 
    [19, 14, 13, 10, 12]
  ]
  tex = [
    [56 / 300, 0],
    [244 / 300, 0],
    [1, 174 / 300],
    [0.5, 283 / 300],
    [0, 174 / 300]
  ]
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
    glRotate(20, 0, 1, 0)
    
    glutSpecialFunc(self.newMotion)
    glutReshapeFunc(self.resizeWindow) # Устанавливаем функцию, которая должна вызываться при изменении размеров окна
    glutDisplayFunc(self.showScreen) # Устанавливаем какая функция будет заниматься отрисовкой в окне
    glutIdleFunc(self.showScreen) # Устанавливаем какую функцию вызывать пока не будет какого-то вызова извне
    # glutMainLoop()  # Запускаем бесконечный цикл работы программы
  




  def mySolidCube(self):
    glBegin(GL_QUADS)
    # Front Face
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0) 
    glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 0) 
    glVertex3f( 1, -1, 1)
    glTexCoord2f(1, 1) 
    glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 1) 
    glVertex3f(-1, 1, 1)

    # Back Face
    glNormal3f(0, 0, -1)
    glTexCoord2f(1, 0) 
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 1) 
    glVertex3f(-1, 1, -1)
    glTexCoord2f(0, 1) 
    glVertex3f( 1, 1, -1)
    glTexCoord2f(0, 0) 
    glVertex3f( 1, -1, -1)

    # Top Face
    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 1) 
    glVertex3f(-1, 1, -1)
    glTexCoord2f(0, 0) 
    glVertex3f(-1, 1, 1)
    glTexCoord2f(1, 0) 
    glVertex3f( 1, 1, 1)
    glTexCoord2f(1, 1) 
    glVertex3f( 1, 1, -1)

    # Bottom Face
    glNormal3f(0, -1, 0)
    glTexCoord2f(1, 1) 
    glVertex3f(-1, -1, -1)
    glTexCoord2f(0, 1) 
    glVertex3f( 1, -1, -1)
    glTexCoord2f(0, 0) 
    glVertex3f( 1, -1, 1)
    glTexCoord2f(1, 0) 
    glVertex3f(-1, -1, 1)

    # Right face
    glNormal3f(1, 0, 0)
    glTexCoord2f(1, 0) 
    glVertex3f( 1, -1, -1)
    glTexCoord2f(1, 1) 
    glVertex3f( 1, 1, -1)
    glTexCoord2f(0, 1) 
    glVertex3f( 1, 1, 1)
    glTexCoord2f(0, 0) 
    glVertex3f( 1, -1, 1)

    # Left Face
    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0) 
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0) 
    glVertex3f(-1, -1, 1)
    glTexCoord2f(1, 1) 
    glVertex3f(-1, 1, 1)
    glTexCoord2f(0, 1) 
    glVertex3f(-1, 1, -1)
    glEnd()

  def myDodecahedron(self):
    glPushMatrix()
    for face in range(12):
      glBegin(GL_POLYGON)
      glNormal3dv(self.normal_vectors[face])
      point = 0
      for vertex in self.faces[face]:
        glTexCoord2dv(self.tex[point])
        glVertex3dv(self.ver[vertex], 0)
        point += 1
      glEnd()
    glPopMatrix()

  def loadTexture(self, figure = 'cube'):
    self.img = Image.open(figure + '.png')	
    width = self.img.width
    height = self.img.height
    self.texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img.tobytes('raw', 'RGBA', 0, -1))
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindTexture(GL_TEXTURE_2D, self.texture)
    
  def drawCube(self, side = 1, position = [0, 0, 0], rotation = [0, 0, 0, 0], ):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 120) 
    glTranslate(position[0], position[1], position[2])
    glRotatef(rotation[0], rotation[1], rotation[2], rotation[3])
    glScalef(side / 2, side / 2, side / 2) # Изменяем размер фигуры в указанное количество раз по осям x, y, z
    self.mySolidCube()
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawDodecahedron(self, outerR = 1, position = [0, 0, 0], spin = [0, 0, 0, 0], throtle = [0, 0, 0, 0]):
    outerR *= 0.58
    glPushMatrix()
    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50) 
    glTranslate(position[0], position[1], position[2])
    glRotate(throtle[0], throtle[1], throtle[2], throtle[3])
    glRotate(spin[0], spin[1], spin[2], spin[3])
    glScalef(outerR, outerR, outerR)
    self.myDodecahedron()
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopMatrix()
    glPopMatrix()

  def drawSphere(self, r = 1):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    glTranslatef(0, 0, 0)
    glutSolidSphere(r, 100, 100) # Отрисовываем каркасную сферу
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
  
  def drawGround(self):
    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 0.5, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 80)
    glBegin(GL_POLYGON)
    glNormal3f(0, 1, 0)
    glVertex3f(10, -0.11, 0)
    glVertex3f(0, -0.11, -10)
    glVertex3f(-10, -0.11, 0)
    glVertex3f(0, -0.11, 10)
    glEnd()
    glPopMatrix()

  def showScreen(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Удаляем все с экрана
    self.moving_speed += self.axeliration * self.seconds_per_frame
    spinning_speed = self.moving_speed / self.dodecR 
    # if self.spinning_angle >= 360:
    #   self.spinning_angle = 0
    # if self.throtle_angle >= 360:
    #   self.throtle_angle = 0
    # if self.moving_speed <= 0:
    #   self.moving_speed = 0
    #   self.axeliration = 0
    #   spinning_speed = 0
    
    self.moving_angle += self.moving_speed * self.seconds_per_frame / self.moving_radius
    self.spinning_angle += math.degrees(spinning_speed * self.seconds_per_frame)
    self.throtle_angle += math.degrees(self.moving_speed * self.seconds_per_frame / self.moving_radius)
    self.dodecX = self.moving_radius * math.cos(self.moving_angle) 
    self.dodecZ = self.moving_radius * math.sin(self.moving_angle)
    # print('\nmoving_speed :', self.moving_speed, \
    #       '\nself.moving_angle :', self.moving_angle, \
    #       '\nself.spinning_angle :', self.spinning_angle, \
    #       '\nself.throtle_angle :', self.throtle_angle, \
    #       '\nself.dodecX :', self.dodecX, \
    #       '\nself.dodecZ :', self.dodecZ, '\n')
    dodec_throtle = [-self.throtle_angle, 0, 1, 0]
    dodec_spin = [self.spinning_angle, 1, 0, 0]
    # dodec_trans = [0, self.dodecR * 0.9, self.moving_radius]
    dodec_trans = [self.dodecX, self.dodecR * 0.999, self.dodecZ]
    
    self.loadTexture(figure = 'cube')
    self.drawCube(side = self.cubeSide, position=[0, self.cubeSide / 2, 0])

    self.loadTexture(figure = 'dodecohedron')
    self.drawDodecahedron(outerR = self.dodecR, position = dodec_trans, spin=dodec_spin, throtle=dodec_throtle)
    self.drawGround()
    # self.drawAxis()
    # glRotatef(1, 0, 1, 0)
    glutSwapBuffers() 



  def resizeWindow(self, width = 800, height = 800):
    size = int((width + height) / 2) # Формируем сторону для окна
    glutReshapeWindow(size, size) # Изменяем размер окна в соответствии с новыми значениями
    glViewport(0, 0, size, size) # Устанавливаем окно, на которое проецируется изображение
    glMatrixMode(GL_PROJECTION) # Далее настриваем отображение
    glLoadIdentity() # Возвращаем марицу в состояние по-умолчанию
    glOrtho(-10, 10, -10, 10, -100, 100)  # Устанавливаем параметры для ортографической проекции
    # glFrustum(-1, 1, -1, 1, 1, 100)
    gluLookAt(0, 0, 5, # Устанавливаем положение камеры x, y, z
              0, 0, 0, # Устанавливаем смещение направления камеры
              0, 1, 0) # Устанавливаем какая ось смотри вверх
    glMatrixMode(GL_MODELVIEW)
    
  def newMotion(self, key, x, y):
    if key == GLUT_KEY_UP:
      self.axeliration += 1
    elif key == GLUT_KEY_DOWN:
      self.axeliration -= 1
    elif key == GLUT_KEY_LEFT or key == GLUT_KEY_RIGHT:
      self.axeliration = 0

  def __call__(self):
    glutMainLoop()

if __name__ == '__main__':
  Kurs().__call__()