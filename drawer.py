from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Drawer:
  cubeSize = 10
  sphereRadius = 3
  torusInnerRadius = 0.5
  torusOuterRadius = 1
  shrinker = 1

  def __init__(self, windoww = 800, windowh = 800):
    glutInit() # Инициализация GLUT для управления окном
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH) # Режимы отображения: два буфера, RGB для вывода цвета, 
    glutInitWindowSize(windoww, windowh)   # Установка высоты и ширины окна
    glutInitWindowPosition(0, 0)   # Положение окна на экране
    glutCreateWindow(b'Cube') # Название окна
    # glClearColor(0.5, 0.5, 0.1, 0) # Задний фон 

    # glEnable(GL_BLEND);
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST) # Включаем буфер глубины
    glEnable(GL_LIGHTING) # Включаем освещение, чтобы получаить разноцветные фигуры
    glEnable(GL_LIGHT0) # Включаем источник света
    glLightfv(GL_LIGHT0, GL_POSITION, [10, 10, 10, 1]) # Помещаем источник света
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0, 0, 0]) # Направляем источник света 
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1]) # Белый свет, отражаемый от поверхностей
    glMaterialf(GL_FRONT, GL_SHININESS, 128) # Степень отрженности света 0-128
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) # Двусторонняя модель света

    glRotate(50, 1, 1, 1) # Повроачиваем все оси на 50 градус

    glutReshapeFunc(self.resizeWindow) # Устанавливаем функцию, которая должна вызываться при изменении размеров окна
    glutDisplayFunc(self.showScreen) # Устанавливаем какая функция будет заниматься отрисовкой в окне
    glutIdleFunc(self.showScreen) # Устанавливаем какую функцию вызывать пока не будет какого-то вызова извне
    
    # glutMainLoop()  # Запускаем бесконечный цикл работы программы

  def drawCube(self):
    # Следующий if-elif отвечает за постоянное изменение размеров куба
    if self.cubeSize >= 10:
      self.shrinker = 0.99
    elif self.cubeSize < 1:
      self.shrinker = 1.01
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glScalef(self.shrinker, self.shrinker, self.shrinker) # Изменяем размер фигуры в указанное количество раз по осям x, y, z
    # self.cubeSize *= self.shrinker # Изменяем ребро куба в указанное количество раз
    glutWireCube(self.cubeSize) # Отрисовываем каркасный куб с установками
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawSphere(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glutWireSphere(self.sphereRadius, 50, 50) # Отрисовываем каркасную сферу
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawTorus(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 0.7]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glTranslatef(self.cubeSize / 2, self.cubeSize / 2, self.cubeSize / 2) # Перемещаем центр тора на вершину куба
    glRotatef(90, 1, 0, 0) # Поворачиваем тор на 90 градусов по оси x 
    # glScalef(self.shrinker, self.shrinker, self.shrinker)
    # self.torusInnerRadius *= self.shrinker
    # self.torusOuterRadius *= self.shrinker
    glutSolidTorus(self.torusInnerRadius, self.torusOuterRadius, 50, 50) # Отрисовываем тор
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawAxis(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glBegin(GL_LINES) # Настраиваем линии для отрисовки 
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, 0) # От центра
    glVertex3f(999, 0, 0) # до 20 по оси x

    glMaterialfv(GL_FRONT_AND_BACK,  GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, 0) # От центра
    glVertex3f(0, 999, 0) # до 20 по оси y

    glMaterialfv(GL_FRONT_AND_BACK,  GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, 0) # От центра
    glVertex3f(0, 0, 999) # до 20 по оси z
    glEnd() # Останавливаем настройку и отрисовываем
    glPopMatrix() # Восстанавливаем положение оси координат
  
  def showScreen(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Удаляем все с экрана
    
    self.drawCube() # Рисуем куб
    self.drawSphere() # Рисуем сферу
    self.drawTorus() # Рисуем тор
    self.drawAxis() # Рисуем оси

    glutSwapBuffers() # Подменяем изображение на экране с новыми настройками



  def resizeWindow(self, width, height):
    size = int((width + height) / 2) # Формируем сторону для окна
    glutReshapeWindow(size, size) # Изменяем размер окна в соответствии с новыми значениями
    glViewport(0, 0, size, size) # Устанавливаем окно, на которое проецируется изображение
    glMatrixMode(GL_PROJECTION) # Далее настриваем отображение
    glLoadIdentity() # Возвращаем марицу в состояние по-умолчанию
    glOrtho(-10, 10, -10, 10, 0, 100)  # Устанавливаем параметры для ортографической проекции
    # glFrustum(-1, 1, -1, 1, 1, 100)
    gluLookAt(0, 0, 10, # Устанавливаем положение камеры x, y, z
              0, 0, 0, # Устанавливаем смещение направления камеры
              0, 1, 0) # Устанавливаем какая ось смотри вверх
    glMatrixMode(GL_MODELVIEW)

  def __call__(self):
    glutMainLoop()