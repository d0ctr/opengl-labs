from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys


def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0,0.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glutWireSphere(2, 20, 10)
    # glTranslate(1,2,1);
    # color = [1.0, 1.0, 0., 1.]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
    # glutSolidCube(2)
    # glTranslate(-2, -2, -2);

    # glTranslate(0, 5, 0);

    glutWireCylinder(2,4,20,30)

    glPopMatrix()
    glRotate(1, 0, 1, 1)
    glutSwapBuffers()

def resizeWindow(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-height/20, height/20, -width/20, width/20, 0, 100)
    gluLookAt(0, 0, 5,
              0, 0, 0,
              0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(700,700)
    glutCreateWindow(b'sphere')
    glClearColor(1.,1.,1.,0.1)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    # lightZeroPosition = [0.,0.,0.,1.]
    # lightZeroColor = [0.8,1.0,0.8,1.0]
    # glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    # glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    # glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    # glEnable(GL_LIGHT0)
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(resizeWindow)
    # glMatrixMode(GL_PROJECTION)
    # gluPerspective(60.,1.,1.,60.)
    # glMatrixMode(GL_MODELVIEW)
    # gluLookAt(0,0,20,
    #           0,0,0,
    #           0,1,0)
    # glPushMatrix()
    glutMainLoop()

    

main()