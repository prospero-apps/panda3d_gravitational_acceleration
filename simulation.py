# file name: pm1E1.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, TextNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText
import simplepbr

class TestApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        base.setBackgroundColor(.53, .81, .92)
        simplepbr.init()       
        props = WindowProperties()
        props.setSize(1200, 675)
        base.win.requestProperties(props)

        # planets and other objects
        objects = [('Jupiter', -25.93),
                   ('Earth', -9.81),
                   ('Mars', -3.73),
                   ('Moon', -1.63),
                   ('Pluto', -.61)]

        # Bullet worlds
        self.worlds = []
        for i in range(len(objects)):
            world = BulletWorld()
            world.setGravity(Vec3(0, 0, objects[i][1]))
            self.worlds.append(world)

        # ground
        shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        node = BulletRigidBodyNode('Ground')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setPos(0, 50, -12)

        # Attach RigidBody to each world.
        for world in self.worlds:
            world.attachRigidBody(node)  

        # Load the terrain model and scale it down on
        # the Z axis to flatten it.          
        terrain = loader.loadModel('terrain/terrain.gltf')
        terrain.setScale(1, 1, .1)
        terrain.reparentTo(np)

        # soccer balls
        # ball model
        ball = loader.loadModel('ball/scene.gltf')

        # instance and position the balls
        for world in self.worlds:
            shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5)) 
            node = BulletRigidBodyNode('')
            node.setMass(1.0)
            node.addShape(shape)
            np = render.attachNewNode(node)
            np.setPos(-20 + self.worlds.index(world) * 10, 50, 5)
            world.attachRigidBody(node)
            ball.instanceTo(np)   
            
            # onscreen text
            x = np.getX() / 15
            obj = objects[self.worlds.index(world)]
            txt = f'{obj[0]}\n{str(abs(obj[1]))} m/s2'
            OnscreenText(text=txt, 
                         pos=(x, .8),
                         scale=.1, 
                         align=TextNode.ACenter)            

        taskMgr.add(self.update, 'update')

    # Update
    def update(self, task):
        dt = globalClock.getDt()

        for world in self.worlds:
            world.doPhysics(dt)
        return task.cont   

app = TestApp()
app.run()