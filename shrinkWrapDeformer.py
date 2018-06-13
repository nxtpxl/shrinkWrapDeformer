  
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
class BoundingBox():
     
    def __init__(self):
        pass
        
    def copyPivot (self, sourceObj, targetObj):
        sourceObj = cmds.ls(sl = True)[len(cmds.ls(sl = True))-1]
        targetObj = cmds.ls(sl = True)[0:(len(cmds.ls(sl = True))-1)]
        parentList = []
        for obj in targetObj:
            print obj
            if cmds.listRelatives( obj, parent = True):
                parentList.append(cmds.listRelatives( obj, parent = True)[0])
            else:
                parentList.append('')
        if len(cmds.ls(sl = True))<2:
            cmds.error('select 2 or more objects.')
        pivotTranslate = cmds.xform (sourceObj, q = True, ws = True, rotatePivot = True)
        cmds.parent(targetObj, sourceObj)
        cmds.makeIdentity(targetObj, a = True, t = True, r = True, s = True)
        cmds.xform (targetObj, ws = True, pivots = pivotTranslate)
        for ind in range(len(targetObj)):
            if parentList[ind] != '' : 
                cmds.parent(targetObj[ind], parentList[ind])
            else:
                cmds.parent(targetObj[ind], world = True)

    def wrapIt(self, *args):
        slMsh = cmds.ls(sl = True)
        mesh = []
        if len(slMsh) >=2:
            for each in slMsh:
                cmds.select(each, add=True )
            name = each+'_g'
            importedCombinedMesh = cmds.polyUnite( n=name )
            cmds.delete( importedCombinedMesh, ch = True )    
            mesh.append(name)
        else:
            for each in slMsh:
                cmds.select(each, add=True )            
                obj = cmds.ls(sl=True)
                print (obj)
                name = cmds.rename(obj[0], (each+'_g'))  
                mesh.append(name)  
        bbox = cmds.exactWorldBoundingBox(mesh[0])        
        x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(mesh[0])
        lowRes = mesh[0] + '_proxyGeo'
        proxymesh = cmds.polySphere(n = lowRes, subdivisionsX = 15, subdivisionsY = 15)
        print proxymesh
        xc = (x2 + x1) / 2.0
        yc = (y2 + y1) / 2.0
        zc = (z2 + z1) / 2.0
        xw = x2 - x1
        yw = y2 - y1
        zw = z2 - z1   
        cmds.move(xc, yc, zc, proxymesh)
        cmds.scale(xw, yw, zw, proxymesh) 
        shrinkWrapNode = pm.deformer(proxymesh, type='shrinkWrap')[0]
        pm.PyNode(name).worldMesh[0] >> shrinkWrapNode.targetGeom
        shrinkWrapNode.closestIfNoIntersection.set(True)   
        cmds.delete( proxymesh, ch = True )  
        cmds.select(clear = True)
        cmds.select(proxymesh[0]) 
        cmds.select(mesh[0], add = True)      
        self.copyPivot(mesh[0], proxymesh)
        #return proxymesh[0]

    def MakeCube(self, *args):
        geo = cmds.geomToBBox(keepOriginal=True, name="bakedBOX", combineMesh = True)
        return geo
        
            
        
