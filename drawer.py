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
  def __init__(self, windoww = 500, windowh = 500):git a
    glutInit() # Инициализация GLUT для управления окном
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) # Режимы отображения: два буфера, RGB для вывода цвета, 
    glutInitWindowSize(windoww, windowh)   # Установка высоты и ширины окна
    glutInitWindowPosition(0, 0)   # Положение окна на экране
    glutCreateWindow(b'Cube') # Название окна
    glClearColor(1, 1, 1, 0) # Задний фон 

    glEnable(GL_LIGHTING) # Включаем освещение, чтобы получаить разноцветные фигуры
    glutReshapeFunc(self.resizeWindow) # Устанавливаем функцию, которая должна вызываться при изменении размеров окна
    glutDisplayFunc(self.showScreen) # Устанавливаем какая функция будет заниматься отрисовкой в окне
    glutIdleFunc(self.showScreen) # Устанавливаем какую функцию вызывать пока не будет какого-то вызова извне
    
    glutMainLoop()  # Запускаем бесконечный цикл работы программы

  def drawCube(self):
    # Следующий if-elif отвечает за постоянное изменение размеров куба
    if self.cubeSize >= 10:
      self.shrinker = 0.99
    elif self.cubeSize < 1:
      self.shrinker = 1.01
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1, 0, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glScalef(self.shrinker, self.shrinker, self.shrinker) # Изменяем размер фигуры в указанное количество раз по осям x, y, z
    self.cubeSize *= self.shrinker # Изменяем ребро куба в указанное количество раз
    glutWireCube(self.cubeSize) # Отрисовываем каркасный куб с установками
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawSphere(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glutWireSphere(self.sphereRadius, 20, 20) # Отрисовываем каркасную сферу
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawTorus(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 1, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glTranslatef(self.cubeSize / 2, self.cubeSize / 2, self.cubeSize / 2) # Перемещаем центр тора на вершину куба
    glRotatef(90, 1, 0, 0) # Поворачиваем тор на 90 градусов по оси x 
    glutSolidTorus(self.torusInnerRadius, self.torusOuterRadius, 20, 20) # Отрисовываем тор
    glPopMatrix() # Восстанавливаем положение оси координат

  def drawAxis(self):
    glPushMatrix() # Запоминаем нынешнее положение оси координат
    glBegin(GL_LINES) # Настраиваем линии для отрисовки 
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1, 0, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, 0) # От центра
    glVertex3f(20, 0, 0) # до 20 по оси x

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 1, 0, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, 0) # От центра
    glVertex3f(0, 20, 0) # до 20 по оси y

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 1, 1]) # Устанавливаем цвет фигуры (RGB, 0-1) и принцип свечения (материал сам производит свет)
    glVertex3f(0, 0, 0) # От центра
    glVertex3f(0, 0, 20) # до 20 по оси z
    glEnd() # Останавливаем настройку и отрисовываем
    glPopMatrix() # Восстанавливаем положение оси координат
  
  def showScreen(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Удаляем все с экрана
    
    self.drawCube() # Рисуем куб
    self.drawSphere() # Рисуем сферу
    self.drawTorus() # Рисуем тор
    self.drawAxis() # Рисуем оси
    
    glRotate(1, 1, 1, 1) # Повроачиваем все оси на 1 градус
    glutSwapBuffers() # Подменяем изображение на экране с новыми настройками



  def resizeWindow(self, width, height):
    size = int((width + height) / 2) # Формируем сторону для окна
    glutReshapeWindow(size, size) # Изменяем размер окна в соответствии с новыми значениями
    glViewport(0, 0, size, size) # Устанавливаем окно, на которое проецируется изображение
    glMatrixMode(GL_PROJECTION) # Далее настриваем отображение
    glLoadIdentity() # Возвращаем марицу в состояние по-умолчанию
    glOrtho(-10, 10, -10, 10, 0, 100)  # Устанавливаем параметры для ортографической проекции
    gluLookAt(0, 0, 10, # Устанавливаем положение камеры x, y, z
              0, 0, 0, # Устанавливаем смещение направления камеры
              0, 1, 0) # Устанавливаем какая ось смотри вверх
    glMatrixMode(GL_MODELVIEW)