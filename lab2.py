
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math

class Lab2:
  rLight = 30
  cubeSize = 5
  sphereRadius = 6
  torusInnerRadius = 1.5
  torusOuterRadius = 4
  moving_speed = 0.05
  position = 0
  img = []
  texture = 0

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
    glLightfv(GL_LIGHT0, GL_POSITION, [20, 20, 20, 1]) # Помещаем источник света
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0, 0, 0]) # Направляем источник света 
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

  def loadTexture(self):
    self.img = Image.open('cobblestone1.png')	
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
    
  def drawTetrahedron(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 5)
    glTranslatef(0, 0, -15)
    glScale(6, 6, 6)
    glRotate(-80, 1, 1, 0)
    glutSolidTetrahedron() # Отрисовываем каркасную сферу
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawCube(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1]) 
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50) 
    glTranslatef(-15, 0, 0)
    glRotatef(45, 1, 1, 1)
    glScalef(self.cubeSize / 2, self.cubeSize / 2, self.cubeSize / 2) # Изменяем размер фигуры в указанное количество раз по осям x, y, z
    self.mySolidCube()
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawSphere(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 0.5])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 0, 1, 0.5]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    glTranslatef(15, 0, 0)
    glutSolidSphere(self.sphereRadius, 100, 100) # Отрисовываем каркасную сферу
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawTorus(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0, 1, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 128) 
    glTranslatef(0, 0, 15) 
    glRotatef(90, 1, 0, 0) # Поворачиваем тор на 90 градусов по оси x
    glutSolidTorus(self.torusInnerRadius, self.torusOuterRadius, 100, 100) # Отрисовываем тор
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawAxis(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
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
    glPopMatrix() # Восстанавливаем положение оси координат
  
  def showScreen(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Удаляем все с экрана
    self.position += self.moving_speed
    glLightfv(GL_LIGHT0, GL_POSITION, [self.rLight * math.cos(self.position ), 30, self.rLight * math.sin(self.position), 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [math.cos(self.position)/2 + 0.5, math.cos(self.position + math.pi)/2 + 0.5, math.cos(self.position + math.pi/2)/2 + 0.5, 1])
    self.loadTexture()
    glBindTexture(GL_TEXTURE_2D, self.texture)
    self.drawCube() # Рисуем куб
    glBindTexture(GL_TEXTURE_2D, 0)
    self.drawTorus() # Рисуем тор
    self.drawTetrahedron()
    self.drawSphere() # Рисуем сферу
    # self.drawAxis() # Рисуем оси
    # glRotate(1, 0, 1, 0)
    glutSwapBuffers() # Подменяем изображение на экране с новыми настройками



  def resizeWindow(self, width, height):
    size = int((width + height) / 2) # Формируем сторону для окна
    glutReshapeWindow(size, size) # Изменяем размер окна в соответствии с новыми значениями
    glViewport(0, 0, size, size) # Устанавливаем окно, на которое проецируется изображение
    glMatrixMode(GL_PROJECTION) # Далее настриваем отображение
    glLoadIdentity() # Возвращаем марицу в состояние по-умолчанию
    glOrtho(-30, 30, -30, 30, -100, 200)  # Устанавливаем параметры для ортографической проекции
    # glFrustum(-1, 1, -1, 1, 1, 100)
    gluLookAt(0, 0, 10, # Устанавливаем положение камеры x, y, z
              0, 0, 0, # Устанавливаем смещение направления камеры
              0, 1, 0) # Устанавливаем какая ось смотри вверх
    glMatrixMode(GL_MODELVIEW)
    

  def __call__(self):
    glutMainLoop()