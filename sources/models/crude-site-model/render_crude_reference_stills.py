import os, math
from pathlib import Path
import vtk
from PIL import Image
from shapely.geometry import Polygon
from shapely.ops import unary_union, triangulate

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT = os.environ.get(
    'CATSKILLS_CRUDE_OUT',
    str(REPO_ROOT / 'sources' / 'images' / 'generated' / 'crude'),
)
os.makedirs(OUT,exist_ok=True)

CX,CZ=56.5,49.0
def X(x): return x-CX
def Z(z): return z-CZ

actors=[]
def reg(a,stage=0,exact_deck_stage=None):
    a._stage=stage
    if exact_deck_stage is not None: a._exact_deck_stage=exact_deck_stage
    actors.append(a)
    return a

def cube(x,z,w,d,h,y=0,color=(.2,.2,.2),stage=0):
    s=vtk.vtkCubeSource(); s.SetXLength(w); s.SetYLength(h); s.SetZLength(d); s.SetCenter(X(x+w/2),y+h/2,Z(z+d/2))
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*color); a.GetProperty().SetInterpolationToPhong();
    return reg(a,stage)

def box_center(cx,cy,cz,w,h,d,color,stage=0,orientation=None):
    s=vtk.vtkCubeSource(); s.SetXLength(w); s.SetYLength(h); s.SetZLength(d)
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.SetPosition(cx,cy,cz); a.GetProperty().SetColor(*color); a.GetProperty().SetInterpolationToPhong()
    if orientation: a.SetOrientation(*orientation)
    return reg(a,stage)

COL={
 'ground':(.67,.63,.52),'siding':(.08,.09,.085),'roof':(.045,.05,.05),'deck':(.65,.43,.25),
 'glass':(.88,.50,.19),'water':(.35,.65,.67),'stone':(.34,.34,.32),'gravel':(.62,.59,.53),
 'wood':(.35,.20,.10),'metal':(.10,.11,.11),'tree':(.18,.30,.16),'trunk':(.20,.13,.08),'fire':(1,.25,.04)
}

# ground
cube(-3.5,-6,120,110,.06,-.06,COL['ground'],0)

def roof_pair(x,z,w,d,eave,rise,stage):
    slope=math.sqrt((d/2)**2+rise**2); ang=math.degrees(math.atan2(rise,d/2)); cx=X(x+w/2)
    box_center(cx,eave+rise/2+.12,Z(z+d*.75),w+.5,.25,slope+.35,COL['roof'],stage,(ang,0,0))
    box_center(cx,eave+rise/2+.12,Z(z+d*.25),w+.5,.25,slope+.35,COL['roof'],stage,(-ang,0,0))

def window_south(x,z,w,h,y,stage): cube(x,z-.10,w,.12,h,y,COL['glass'],stage)
def window_north(x,z,w,h,y,stage): cube(x,z+.01,w,.12,h,y,COL['glass'],stage)
def window_east(x,z,d,h,y,stage): cube(x-.01,z,.12,d,h,y,COL['glass'],stage)
def door_south(x,z,w,h,y,stage): cube(x,z-.12,w,.14,h,y,COL['glass'],stage)

def building(x,z,w,d,h,kind,stage):
    cube(x,z,w,d,h,.10,COL['siding'],stage); roof_pair(x,z,w,d,h+.15,2.7,stage)
    if kind=='main':
        window_south(x+1.3,z,w*.26,4.8,1.65,stage); door_south(x+w*.44,z,3.5,6.7,.25,stage); window_south(x+w*.66,z,w*.25,4.6,1.7,stage)
    elif kind=='bath':
        # Courtyard-facing EAST wall, glass on its northern portion.
        window_east(x+w,z+d*.54,d*.40,5.25,1.55,stage); door_south(x+w*.38,z,3.1,6.5,.2,stage)
    elif kind=='adu':
        window_north(x+1.2,z+d,w*.3,4.8,1.55,stage); window_north(x+w*.55,z+d,w*.35,4.8,1.55,stage)
    elif kind=='guest':
        window_north(x+1.2,z+d,w*.36,4.9,1.4,stage); door_south(x+w*.62,z,3.1,6.4,.25,stage)

def deck_actor(poly,exact_stage):
    pts=vtk.vtkPoints(); cells=vtk.vtkCellArray(); pi=0
    for tri in triangulate(poly):
        if not poly.covers(tri.representative_point()): continue
        ids=[]
        for x,z in list(tri.exterior.coords)[:3]: pts.InsertNextPoint(X(x),.42,Z(z)); ids.append(pi); pi+=1
        c=vtk.vtkTriangle(); [c.GetPointIds().SetId(j,idv) for j,idv in enumerate(ids)]; cells.InsertNextCell(c)
    pd=vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells); mp=vtk.vtkPolyDataMapper(); mp.SetInputData(pd)
    a=vtk.vtkActor(); a.SetMapper(mp); a.GetProperty().SetColor(*COL['deck']); reg(a,exact_stage,exact_stage)
    return a

P2=Polygon([(36,64),(68,64),(68,72),(36,72)])
P4=Polygon([(10,30),(38,30),(38,58),(40,58),(40,72),(36,72),(36,64),(30,64),(30,58),(10,58)])
P6a=Polygon([(38,26),(78,26),(78,34),(74,34),(74,36),(48,36),(48,34),(38,34)])
P6b=Polygon([(48,6),(78,6),(78,34),(48,34)])
P7=Polygon([(26,8),(50,8),(50,34),(38,34),(38,30),(26,30)])
P8a=Polygon([(77,37),(103,37),(103,64),(68,64),(68,58),(77,58)])
P8b=Polygon([(68,34),(78,34),(78,64),(68,64)])
DECKS={2:[P2],4:[P4],6:[P6a,P6b],7:[P7],8:[P8a,P8b]}
for st in [2,4,6,7,8]:
    ps=[]
    for s,arr in DECKS.items():
        if s<=st: ps.extend(arr)
    u=unary_union(ps)
    geoms=[u] if u.geom_type=='Polygon' else list(u.geoms)
    for g in geoms: deck_actor(g,st)

building(40,72,24,20,8.5,'main',1)
building(14,38,16,16,8,'bath',4)
building(52,10,22,20,8.2,'adu',6)
building(31,12,16,12,7.7,'guest',7)

# firepit
fireX,fireZ=54,50
s=vtk.vtkCylinderSource(); s.SetRadius(10.5); s.SetHeight(.10); s.SetResolution(72); s.SetCenter(X(fireX),.08,Z(fireZ)); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*COL['gravel']); reg(a,3)
t=vtk.vtkParametricTorus(); t.SetRingRadius(2.15); t.SetCrossSectionRadius(.55); sf=vtk.vtkParametricFunctionSource(); sf.SetParametricFunction(t); sf.SetUResolution(48); sf.SetVResolution(12); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(sf.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.SetPosition(X(fireX),.55,Z(fireZ)); a.RotateX(90); a.GetProperty().SetColor(*COL['stone']); reg(a,3)
co=vtk.vtkConeSource(); co.SetRadius(.6); co.SetHeight(1.6); co.SetResolution(12); co.SetCenter(X(fireX),1.0,Z(fireZ)); co.SetDirection(0,1,0); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(co.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*COL['fire']); reg(a,3)

# seating stage5
for ang in [15,70,125,195,250,310]:
    r=7.2; rad=math.radians(ang); cx=fireX+r*math.cos(rad); cz=fireZ+r*math.sin(rad)
    cube(cx-.8,cz-.45,1.6,.9,.6,.08,COL['wood'],5)
# cold plunge
cube(31.3,39,4.2,5,1.45,.28,COL['metal'],5); cube(31.65,39.35,3.5,4.3,.08,1.72,COL['water'],5)
# hot tub
for radius,height,y,col in [(3.25,1.65,1.05,COL['wood']),(2.62,.08,1.90,COL['water'])]:
    s=vtk.vtkCylinderSource(); s.SetRadius(radius); s.SetHeight(height); s.SetResolution(48); s.SetCenter(X(25.5),y,Z(34.6)); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*col); reg(a,5)
cube(21.15,33.8,.9,1.6,1.8,.25,COL['metal'],5); cube(21.48,34.35,.22,.22,4.4,1.82,COL['metal'],5)

# outdoor kitchen stage8
kx,kz,kw,kd,kh=81,41,18,16,8
for x,z in [(kx,kz),(kx+kw,kz),(kx,kz+kd),(kx+kw,kz+kd)]: cube(x-.22,z-.22,.44,.44,kh,.18,COL['wood'],8)
roof_pair(kx,kz,kw,kd,kh+.12,2.7,8)
cube(kx+kw-3.2,kz+2,2.4,kd-4,3,.25,COL['wood'],8); cube(kx+2,kz+.8,kw-4,2.0,3,.25,COL['wood'],8); cube(kx+1.0,kz+5.0,1.8,7.0,3,.25,COL['wood'],8)
cube(kx+.75,kz+4.7,2.3,7.6,.30,3.18,COL['stone'],8); cube(kx+kw-2.8,kz+4.0,1.8,3.6,1.4,3.25,COL['metal'],8); cube(kx+kw-2.8,kz+10.2,1.8,3.0,1.9,3.25,COL['metal'],8)

# perimeter trees
def tree(x,z,s=1.0):
    s1=vtk.vtkCylinderSource(); s1.SetRadius(.16*s); s1.SetHeight(4*s); s1.SetResolution(8); s1.SetCenter(X(x),2*s,Z(z)); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(s1.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*COL['trunk']); reg(a,0)
    c=vtk.vtkConeSource(); c.SetRadius(1.3*s); c.SetHeight(4.7*s); c.SetResolution(9); c.SetDirection(0,1,0); c.SetCenter(X(x),5*s,Z(z)); m=vtk.vtkPolyDataMapper(); m.SetInputConnection(c.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(m); a.GetProperty().SetColor(*COL['tree']); reg(a,0)
for x in range(0,111,7): tree(x,0,.8); tree(x,98,.8)
for z in range(7,95,8): tree(0,z,.8); tree(110,z,.8)

ren=vtk.vtkRenderer(); ren.SetBackground(.83,.81,.74)
for a in actors: ren.AddActor(a)
sun=vtk.vtkLight(); sun.SetLightTypeToSceneLight(); sun.SetPosition(-55,75,60); sun.SetFocalPoint(0,0,0); sun.SetColor(1,.82,.62); sun.SetIntensity(1.5); ren.AddLight(sun)
fill=vtk.vtkLight(); fill.SetLightTypeToSceneLight(); fill.SetPosition(55,45,-55); fill.SetFocalPoint(0,0,0); fill.SetColor(.65,.75,.82); fill.SetIntensity(.6); ren.AddLight(fill)

cams={
1:([-4,16.79,1.28],[-4,2,33],44),2:([-4,20.07,-5.99],[-4,2,28],45),3:([23.83,29.46,-30.73],[-2,2,14],46),4:([23.83,33.45,-33.83],[-18,2,8],48),5:([25.99,35.14,-46.99],[-20,2,-1],48),6:([32.65,42.80,-71.55],[0,2,-15],50),7:([-8,28,-70],[-8,2,-15],58),8:([-74,30,-8],[18,2,1],58)}

def set_stage(stage):
    exact=max([s for s in [2,4,6,7,8] if s<=stage],default=None)
    for a in actors:
        if hasattr(a,'_exact_deck_stage'): a.SetVisibility(a._exact_deck_stage==exact)
        else: a.SetVisibility(a._stage<=stage)

def capture(path,w,h,cam):
    win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.AddRenderer(ren); win.SetSize(w,h); win.SetMultiSamples(8)
    ren.SetActiveCamera(cam); win.Render()
    w2i=vtk.vtkWindowToImageFilter(); w2i.SetInput(win); w2i.ReadFrontBufferOff(); w2i.Update()
    wr=vtk.vtkPNGWriter(); wr.SetFileName(path); wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()
    Image.open(path).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(path)
    win.Finalize()

def render_all():
    td=os.path.join(OUT,'top_down'); pr=os.path.join(OUT,'perspectives'); os.makedirs(td,exist_ok=True); os.makedirs(pr,exist_ok=True)
    for stage in range(1,9):
        set_stage(stage)
        cam=vtk.vtkCamera(); cam.SetPosition(0,120,0); cam.SetFocalPoint(0,0,0); cam.SetViewUp(0,0,1); cam.ParallelProjectionOn(); cam.SetParallelScale(50); cam.SetClippingRange(.1,350)
        capture(os.path.join(td,f'stage_{stage:02d}_topdown.png'),1120,1000,cam)
        pos,tgt,fov=cams[stage]; cam2=vtk.vtkCamera(); cam2.SetPosition(*pos); cam2.SetFocalPoint(*tgt); cam2.SetViewUp(0,1,0); cam2.SetViewAngle(fov); cam2.SetClippingRange(.1,350)
        capture(os.path.join(pr,f'stage_{stage:02d}_perspective.png'),1600,1000,cam2)
    return td,pr

if __name__=='__main__':
    print(render_all())
