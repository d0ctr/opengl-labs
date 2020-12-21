from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def resizeWindow(width, height):
    glViewport(0,0,width,height)
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(-5,5, -5,5, 2,12)   
    gluLookAt( 0,0,5, 0,0,0, 0,1,0 )
    glMatrixMode( GL_MODELVIEW )   



def displayWindow():
    front_color = [0,1,0,1]
    back_color = [0,0,1,1]
    front_emission = [1,1,0,1]
    back_emission = [0,0,1,1]

    quadObj = gluNewQuadric() 

    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

    glMaterialfv(GL_FRONT, GL_DIFFUSE, front_color)
    glMaterialfv(GL_BACK, GL_DIFFUSE, back_color)

    #glMaterialfv(GL_FRONT, GL_EMISSION, front_emission)
    #glMaterialfv(GL_BACK, GL_EMISSION, back_emission)

    glPushMatrix()
    glRotated(110, -1,1,0)
    gluCylinder(quadObj, 1, 0.5, 2, 10, 10) 
    glPopMatrix()

    gluDeleteQuadric(quadObj)
    glutSwapBuffers()



def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(700,700)
    glutCreateWindow(b'sphere')
    glClearColor(1.,1.,1.,0.1)

    pos = [3,3,3,1]
    direct = [-1,-1,-1]

    mat_specular = [1,1,1,1 ]



    glEnable(GL_DEPTH_TEST)

    #glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, pos)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direct)


    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, 128.0)

    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

    glutDisplayFunc(displayWindow)
    glutIdleFunc(displayWindow)
    glutReshapeFunc(resizeWindow)
    glutMainLoop()

main()