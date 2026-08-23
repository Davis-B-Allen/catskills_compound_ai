import vtk, math, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union, triangulate

OUT=os.environ.get('CATSKILLS_INTERMEDIATE_OUT', os.path.join(os.path.dirname(__file__), 'generated_intermediate'))
os.makedirs(OUT,exist_ok=True)
random.seed(7)

# ---------- procedural textures ----------
def save_tex(name, img):
    p=os.path.join(OUT,name); img.save(p); return p

def make_wood_deck(size=1024):
    img=Image.new('RGB',(size,size),(154,111,74)); px=img.load()
    for y in range(size):
        plank=(y//46)
        base=(157 + (plank%4-1)*5, 113 + (plank%3-1)*4, 76 + ((plank+1)%3-1)*3)
        for x in range(size):
            noise=random.randint(-8,8)
            grain=int(5*math.sin(x/13+y/61)+3*math.sin(x/4.7))
            px[x,y]=tuple(max(0,min(255,c+noise+grain)) for c in base)
    d=ImageDraw.Draw(img)
    for y in range(0,size,46):
        d.line((0,y,size,y),fill=(67,45,31),width=3)
        d.line((0,y+3,size,y+3),fill=(196,148,103),width=1)
    for y in range(23,size,46):
        for x in range(0,size,160):
            xx=(x+(y*7)%97)%size
            d.ellipse((xx,y-2,xx+5,y+2),fill=(84,53,33))
    return img.filter(ImageFilter.GaussianBlur(.35))

def make_ground(size=1024):
    img=Image.new('RGB',(size,size),(103,104,75)); px=img.load()
    for y in range(size):
        for x in range(size):
            n=random.gauss(0,13)
            s=7*math.sin(x/41)+5*math.sin(y/57)
            px[x,y]=(max(45,min(150,int(101+n+s))),max(50,min(145,int(104+n*.7+s))),max(35,min(110,int(72+n*.4))))
    d=ImageDraw.Draw(img)
    for _ in range(6500):
        x=random.randrange(size); y=random.randrange(size); r=random.choice([1,1,1,2,2,3])
        col=random.choice([(72,78,46),(126,112,79),(66,67,46),(139,127,93),(88,95,54)])
        d.ellipse((x-r,y-r,x+r,y+r),fill=col)
    return img.filter(ImageFilter.GaussianBlur(.6))

def make_gravel(size=1024):
    img=Image.new('RGB',(size,size),(126,120,107)); d=ImageDraw.Draw(img)
    for _ in range(35000):
        x=random.randrange(size); y=random.randrange(size); r=random.choice([1,1,2,2,3,4])
        v=random.randint(80,165); col=(v, max(70,v-4), max(65,v-11))
        d.ellipse((x-r,y-r,x+r,y+r),fill=col)
    return img.filter(ImageFilter.GaussianBlur(.25))

tex_deck_path=save_tex('deck.jpg',make_wood_deck())
tex_ground_path=save_tex('ground.jpg',make_ground())
tex_gravel_path=save_tex('gravel.jpg',make_gravel())

def vtk_texture(path, repeat=True):
    rd=vtk.vtkJPEGReader(); rd.SetFileName(path); rd.Update()
    t=vtk.vtkTexture(); t.SetInputConnection(rd.GetOutputPort()); t.InterpolateOn()
    if repeat: t.RepeatOn()
    return t
TEX_DECK=vtk_texture(tex_deck_path)
TEX_GROUND=vtk_texture(tex_ground_path)
TEX_GRAVEL=vtk_texture(tex_gravel_path)

# ---------- scene helpers ----------
CX,CZ=56.5,49.0
def X(x): return x-CX
def Z(z): return z-CZ

actors=[]
lights=[]
def reg(a,stage=0):
    a._stage=stage; actors.append(a); return a

def pbr(prop, color, rough=.65, metal=.0, emissive=None):
    prop.SetInterpolationToPBR(); prop.SetColor(*color); prop.SetRoughness(rough); prop.SetMetallic(metal)
    if emissive is not None: prop.SetEmissiveFactor(emissive)

def cube(x,z,w,d,h,y=0, color=(.2,.2,.2), rough=.7, metal=0, stage=0, tex=None, opacity=1.0):
    src=vtk.vtkCubeSource(); src.SetXLength(w); src.SetYLength(h); src.SetZLength(d); src.SetCenter(X(x+w/2),y+h/2,Z(z+d/2))
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(src.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); pbr(a.GetProperty(),color,rough,metal); a.GetProperty().SetOpacity(opacity)
    if tex is not None: a.SetTexture(tex)
    return reg(a,stage)

def box_center(cx,cy,cz,w,h,d,color,rough=.7,metal=0,stage=0,orientation=None,opacity=1):
    src=vtk.vtkCubeSource(); src.SetXLength(w); src.SetYLength(h); src.SetZLength(d)
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(src.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); a.SetPosition(cx,cy,cz); pbr(a.GetProperty(),color,rough,metal); a.GetProperty().SetOpacity(opacity)
    if orientation: a.SetOrientation(*orientation)
    return reg(a,stage)

def light(pos,color=(1,.7,.4),intensity=1,stage=0,positional=True):
    l=vtk.vtkLight(); l.SetPosition(*pos); l.SetColor(*color); l.SetIntensity(intensity); l.SetPositional(positional)
    if positional: l.SetConeAngle(110); l.SetAttenuationValues(1,0.04,0.002)
    l._stage=stage; lights.append(l); return l

# ground plane with UVs
pts=vtk.vtkPoints(); pts.InsertNextPoint(-60,0,-55); pts.InsertNextPoint(60,0,-55); pts.InsertNextPoint(60,0,55); pts.InsertNextPoint(-60,0,55)
pol=vtk.vtkPolygon(); pol.GetPointIds().SetNumberOfIds(4)
for i in range(4): pol.GetPointIds().SetId(i,i)
ca=vtk.vtkCellArray(); ca.InsertNextCell(pol)
pd=vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
tc=vtk.vtkFloatArray(); tc.SetNumberOfComponents(2); tc.SetName('TCoords')
for uv in [(0,0),(12,0),(12,11),(0,11)]: tc.InsertNextTuple2(*uv)
pd.GetPointData().SetTCoords(tc)
mapr=vtk.vtkPolyDataMapper(); mapr.SetInputData(pd); ground=vtk.vtkActor(); ground.SetMapper(mapr); ground.SetTexture(TEX_GROUND); pbr(ground.GetProperty(),(.6,.6,.5),1,0); reg(ground,0)

SID=(0.055,0.06,0.06); SID2=(0.09,0.095,0.09); ROOF=(0.055,0.06,0.065); FRAME=(0.035,0.038,0.04); WARM=(1.0,.55,.23)
CEDAR=(.53,.30,.14); STONE=(.32,.31,.29); METAL=(.13,.14,.14); WATER=(.16,.38,.44)

# façade details

def wall_battens(x,z,w,d,h,stage):
    # south/north walls battens every 1.15 ft
    for xx in [x+i*1.15 for i in range(int(w/1.15)+1)]:
        cube(xx,z-.035,.035,.07,h-.15,.12,SID2,.92,0,stage)
        cube(xx,z+d-.035,.035,.07,h-.15,.12,SID2,.92,0,stage)
    for zz in [z+i*1.15 for i in range(int(d/1.15)+1)]:
        cube(x-.035,zz,.07,.035,h-.15,.12,SID2,.92,0,stage)
        cube(x+w-.035,zz,.07,.035,h-.15,.12,SID2,.92,0,stage)

def roof_pair(x,z,w,d,eave,rise,stage):
    slope=math.sqrt((d/2)**2+rise**2); ang=math.degrees(math.atan2(rise,d/2))
    cx=X(x+w/2)
    # north plane
    box_center(cx,eave+rise/2+.13,Z(z+d*.75),w+.55,.22,slope+.4,ROOF,.35,.35,stage,(ang,0,0))
    box_center(cx,eave+rise/2+.13,Z(z+d*.25),w+.55,.22,slope+.4,ROOF,.35,.35,stage,(-ang,0,0))
    # standing seams
    for xx in [x+.25+i*1.35 for i in range(max(1,int(w/1.35)))]:
        for north,sgn in [(True,1),(False,-1)]:
            zz=z+d*.75 if north else z+d*.25
            a=box_center(X(xx),eave+rise/2+.28,Z(zz),.045,.10,slope+.32,(.12,.13,.14),.25,.75,stage,(sgn*ang,0,0))

def window_south(x,z,w,h,y,stage):
    # frame + glowing pane on south face
    cube(x,z-.12,w,.10,h,y,FRAME,.35,.2,stage)
    cube(x+.12,z-.19,w-.24,.06,h-.24,y+.12,(.22,.25,.24),.15,.05,stage,opacity=.72)
    cube(x+.20,z-.25,w-.40,.03,h-.40,y+.20,(1,.45,.14),.5,0,stage)
    # simple mullions
    cube(x+w/2-.035,z-.27,.07,.05,h-.15,y+.08,FRAME,.4,.2,stage)

def window_north(x,z,w,h,y,stage):
    cube(x,z-.02,w,.10,h,y,FRAME,.35,.2,stage)
    cube(x+.12,z+.07,w-.24,.06,h-.24,y+.12,(.22,.25,.24),.15,.05,stage,opacity=.72)
    cube(x+.20,z+.12,w-.40,.03,h-.40,y+.20,(1,.45,.14),.5,0,stage)
    cube(x+w/2-.035,z+.13,.07,.05,h-.15,y+.08,FRAME,.4,.2,stage)

def window_east(x,z,d,h,y,stage,sauna=False):
    cube(x-.02,z,.10,d,h,y,FRAME,.35,.2,stage)
    cube(x+.07,z+.12,.06,d-.24,h-.24,y+.12,(.22,.25,.24),.15,.05,stage,opacity=.74)
    cube(x+.13,z+.20,.03,d-.40,h-.40,y+.20,(1,.43,.12),.45,0,stage)
    if sauna:
        # cedar benches visible behind glass
        cube(x-2.2,z+.7,2.0,d-1.4,.65,2.0,CEDAR,.8,0,stage)
        cube(x-2.1,z+.8,1.9,d-1.6,.55,3.45,CEDAR,.8,0,stage)
        # heater block near north end
        cube(x-1.6,z+d-1.5,1.1,1.1,1.2,.35,(.18,.18,.17),.6,.4,stage)
        light((X(x-1.1),3.4,Z(z+d/2)),(1,.38,.12),2.0,stage)

def door_south(x,z,w=3,h=7,y=.1,stage=1):
    cube(x,z-.14,w,.12,h,y,FRAME,.4,.2,stage)
    cube(x+.18,z-.22,w-.36,.05,h-.35,y+.18,(.25,.25,.24),.15,0,stage,opacity=.68)
    cube(x+.25,z-.28,w-.5,.02,h-.5,y+.25,(1,.42,.14),.6,0,stage)


def building(x,z,w,d,h,kind,stage):
    cube(x,z,w,d,h,.10,SID,.93,0,stage)
    wall_battens(x,z,w,d,h,stage)
    roof_pair(x,z,w,d,h+.15,2.7,stage)
    if kind=='main':
        # courtyard is south
        window_south(x+1.3,z,w*0.26,4.8,1.65,stage)
        door_south(x+w*.44,z,3.5,6.7,.25,stage)
        window_south(x+w*.66,z,w*.25,4.6,1.7,stage)
        light((X(x+w/2),4.0,Z(z-2)),(1,.55,.25),1.3,stage)
    elif kind=='adu':
        # courtyard/north face
        window_north(x+1.2,z+d,w*.3,4.8,1.55,stage)
        window_north(x+w*.55,z+d,w*.35,4.8,1.55,stage)
        light((X(x+w/2),3.8,Z(z+d+1.2)),(1,.55,.25),1.1,stage)
    elif kind=='guest':
        window_north(x+1.2,z+d,w*.36,4.9,1.4,stage)
        door_south(x+w*.62,z,3.1,6.4,.25,stage)
        light((X(x+w/2),3.5,Z(z+d+1)),(1,.5,.22),1.0,stage)
    elif kind=='bath':
        # east-facing courtyard wall; sauna glass on northern portion
        window_east(x+w,z+d*.54,d*.40,5.25,1.55,stage,True)
        # small south entry, hidden mostly in stage4/5 but consistent
        door_south(x+w*.38,z,3.1,6.5,.2,stage)

# ---------- deck geometry ----------
def deck_actor(poly,stage):
    # top triangles from shapely triangulation, filter to polygon interior
    points=vtk.vtkPoints(); cells=vtk.vtkCellArray(); tcoords=vtk.vtkFloatArray(); tcoords.SetNumberOfComponents(2); tcoords.SetName('TCoords')
    pi=0
    tris=triangulate(poly)
    for tri in tris:
        if not poly.covers(tri.representative_point()): continue
        coords=list(tri.exterior.coords)[:3]
        ids=[]
        for x,z in coords:
            points.InsertNextPoint(X(x),.44,Z(z)); tcoords.InsertNextTuple2(x/7.0,z/7.0); ids.append(pi); pi+=1
        cell=vtk.vtkTriangle();
        for j,idv in enumerate(ids): cell.GetPointIds().SetId(j,idv)
        cells.InsertNextCell(cell)
    pd=vtk.vtkPolyData(); pd.SetPoints(points); pd.SetPolys(cells); pd.GetPointData().SetTCoords(tcoords)
    mp=vtk.vtkPolyDataMapper(); mp.SetInputData(pd); a=vtk.vtkActor(); a.SetMapper(mp); a.SetTexture(TEX_DECK); pbr(a.GetProperty(),(.7,.45,.25),.8,0); reg(a,stage)
    # side skirt along boundary rings
    for ring in [poly.exterior,*poly.interiors]:
        cs=list(ring.coords)
        for (x1,z1),(x2,z2) in zip(cs[:-1],cs[1:]):
            dx=x2-x1; dz=z2-z1; L=math.hypot(dx,dz)
            if L<.01: continue
            mx=X((x1+x2)/2); mz=Z((z1+z2)/2); ang=-math.degrees(math.atan2(dz,dx))
            box_center(mx,.25,mz,L,.38,.16,(.31,.17,.09),.85,0,stage,(0,ang,0))
    return a

P2=Polygon([(36,64),(68,64),(68,72),(36,72)])
P4=Polygon([(10,30),(38,30),(38,58),(40,58),(40,72),(36,72),(36,64),(30,64),(30,58),(10,58)])
P6a=Polygon([(38,26),(78,26),(78,34),(74,34),(74,36),(48,36),(48,34),(38,34)])
P6b=Polygon([(48,6),(78,6),(78,34),(48,34)])
P7=Polygon([(26,8),(50,8),(50,34),(38,34),(38,30),(26,30)])
P8a=Polygon([(77,37),(103,37),(103,64),(68,64),(68,58),(77,58)])
P8b=Polygon([(68,34),(78,34),(78,64),(68,64)])
DECK_STAGE_POLYS={2:[P2],4:[P4],6:[P6a,P6b],7:[P7],8:[P8a,P8b]}
# Render each stage as union of all deck components present by then, with ONE clean surface.
deck_stage_actors={}
for st in [2,4,6,7,8]:
    allps=[]
    for s,ps in DECK_STAGE_POLYS.items():
        if s<=st: allps.extend(ps)
    u=unary_union(allps)
    if u.geom_type=='Polygon': deck_stage_actors[st]=[deck_actor(u,st)]
    else: deck_stage_actors[st]=[deck_actor(g,st) for g in u.geoms]
    # these stage-specific union decks should only show at exactly that stage range; manage separately below
    for a in deck_stage_actors[st]: a._exact_deck_stage=st

# buildings
building(40,72,24,20,8.5,'main',1)
building(14,38,16,16,8,'bath',4)
building(52,10,22,20,8.2,'adu',6)
building(31,12,16,12,7.7,'guest',7)

# Firepit stage3
fireX,fireZ=54,50
# gravel disc mesh
src=vtk.vtkCylinderSource(); src.SetRadius(10.5); src.SetHeight(.10); src.SetResolution(96); src.SetCenter(X(fireX),.08,Z(fireZ)); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); pad=vtk.vtkActor(); pad.SetMapper(mp); pad.SetTexture(TEX_GRAVEL); pbr(pad.GetProperty(),(.6,.58,.53),1,0); reg(pad,3)
# ring stone torus
tr=vtk.vtkParametricTorus(); tr.SetRingRadius(2.15); tr.SetCrossSectionRadius(.55); tf=vtk.vtkParametricFunctionSource(); tf.SetParametricFunction(tr); tf.SetUResolution(72); tf.SetVResolution(18); mm=vtk.vtkPolyDataMapper(); mm.SetInputConnection(tf.GetOutputPort()); ring=vtk.vtkActor(); ring.SetMapper(mm); ring.SetPosition(X(fireX),.55,Z(fireZ)); ring.RotateX(90); pbr(ring.GetProperty(),STONE,.98,0); reg(ring,3)
# inner dark basin and flame
cube(fireX-1.45,fireZ-1.45,2.9,2.9,.22,.16,(.10,.09,.08),1,0,3)
cone=vtk.vtkConeSource(); cone.SetRadius(.65); cone.SetHeight(1.8); cone.SetResolution(16); cone.SetCenter(X(fireX),1.05,Z(fireZ)); cone.SetDirection(0,1,0); mm=vtk.vtkPolyDataMapper(); mm.SetInputConnection(cone.GetOutputPort()); flame=vtk.vtkActor(); flame.SetMapper(mm); pbr(flame.GetProperty(),(1,.18,.03),.35,0,(2.7,.65,.15)); reg(flame,3); light((X(fireX),3.0,Z(fireZ)),(1,.28,.08),3.2,3)

# Stage5 seating
for ang in [15,70,125,195,250,310]:
    r=7.2; rad=math.radians(ang); cx=fireX+r*math.cos(rad); cz=fireZ+r*math.sin(rad)
    # simple Adirondack-ish chair: seat/back/arms, rotated tangentially toward fire
    yaw=math.degrees(math.atan2(fireZ-cz,fireX-cx))
    a=box_center(X(cx),.52,Z(cz),1.8,.28,1.15,(.30,.18,.10),.85,0,5,(0,-yaw,0))
    # back
    back=box_center(X(cx)-.35*math.cos(rad),1.25,Z(cz)-.35*math.sin(rad),1.75,1.4,.18,(.30,.18,.10),.85,0,5,(0,-yaw, -10))

# Cold plunge stage5: east of southern half bathhouse
cube(31.3,39,4.2,5,1.45,.28,METAL,.42,.35,5)
cube(31.65,39.35,3.5,4.3,.08,1.72,WATER,.18,.05,5)
# Hot tub stage5: cedar cylinder south and west of plunge
src=vtk.vtkCylinderSource(); src.SetRadius(3.25); src.SetHeight(1.65); src.SetResolution(64); src.SetCenter(X(25.5),1.05,Z(34.6)); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); tub=vtk.vtkActor(); tub.SetMapper(mp); pbr(tub.GetProperty(),(.40,.21,.10),.8,0); reg(tub,5)
src=vtk.vtkCylinderSource(); src.SetRadius(2.62); src.SetHeight(.08); src.SetResolution(64); src.SetCenter(X(25.5),1.90,Z(34.6)); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); wt=vtk.vtkActor(); wt.SetMapper(mp); pbr(wt.GetProperty(),WATER,.15,.05); reg(wt,5)
# metal bands on tub
for yy in [.55,1.15,1.72]:
    tor=vtk.vtkParametricTorus(); tor.SetRingRadius(3.22); tor.SetCrossSectionRadius(.055); src=vtk.vtkParametricFunctionSource(); src.SetParametricFunction(tor); src.SetUResolution(64); src.SetVResolution(8); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(mp); a.SetPosition(X(25.5),yy,Z(34.6)); a.RotateX(90); pbr(a.GetProperty(),(.22,.23,.23),.35,.65); reg(a,5)
# stove/chimney
cube(21.15,33.8,.9,1.6,1.8,.25,(.10,.11,.11),.38,.7,5)
cube(21.48,34.35,.22,.22,4.4,1.82,(.10,.11,.11),.30,.75,5)

# Stage8 open kitchen pavilion
kx,kz,kw,kd,kh=81,41,18,16,8
for x,z in [(kx,kz),(kx+kw,kz),(kx,kz+kd),(kx+kw,kz+kd)]: cube(x-.22,z-.22,.44,.44,kh,.18,(.24,.14,.08),.8,0,8)
roof_pair(kx,kz,kw,kd,kh+.12,2.7,8)
# back/right cabinetry and west-facing bar edge
cube(kx+kw-3.2,kz+2,2.4,kd-4,3,.25,(.20,.13,.09),.75,0,8)
cube(kx+2,kz+.8,kw-4,2.0,3,.25,(.20,.13,.09),.75,0,8)
cube(kx+1.0,kz+5.0,1.8,7.0,3,.25,(.32,.19,.10),.7,0,8)
# counter slab
cube(kx+.75,kz+4.7,2.3,7.6,.30,3.18,(.36,.34,.31),.35,.1,8)
# grill/smoker forms
cube(kx+kw-2.8,kz+4.0,1.8,3.6,1.4,3.25,(.18,.19,.19),.25,.75,8)
cube(kx+kw-2.8,kz+10.2,1.8,3.0,1.9,3.25,(.09,.09,.09),.45,.55,8)
# stools along courtyard-facing west bar
for zz in [46,49,52,55]:
    cube(kx-.8,zz,.55,.55,1.6,.20,(.26,.15,.08),.82,0,8)
    src=vtk.vtkCylinderSource(); src.SetRadius(.38); src.SetHeight(.15); src.SetResolution(20); src.SetCenter(X(kx-.52),1.85,Z(zz+.28)); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(mp); pbr(a.GetProperty(),(.28,.16,.09),.8,0); reg(a,8)
light((X(kx+6),5.8,Z(kz+8)),(1,.50,.20),1.7,8)

# perimeter conifers (always)
def conifer(x,z,s=1.0):
    # trunk
    src=vtk.vtkCylinderSource(); src.SetRadius(.18*s); src.SetHeight(4.3*s); src.SetResolution(10); src.SetCenter(X(x),2.15*s,Z(z)); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); a=vtk.vtkActor(); a.SetMapper(mp); pbr(a.GetProperty(),(.20,.12,.07),1,0); reg(a,0)
    # layered cones
    for i,(yy,r,h) in enumerate([(3.3,1.5,3.7),(4.7,1.25,3.2),(5.9,.95,2.8)]):
        src=vtk.vtkConeSource(); src.SetRadius(r*s); src.SetHeight(h*s); src.SetResolution(12); src.SetDirection(0,1,0); src.SetCenter(X(x),yy*s,Z(z)); mp=vtk.vtkPolyDataMapper(); mp.SetInputConnection(src.GetOutputPort()); c=vtk.vtkActor(); c.SetMapper(mp); pbr(c.GetProperty(),(.10+.018*i,.22+.018*i,.10),1,0); reg(c,0)

# irregular forest perimeter / background
for x in range(0,111,7):
    conifer(x,0,.75+random.random()*.35); conifer(x,98,.75+random.random()*.4)
for z in range(7,95,8):
    conifer(0,z,.75+random.random()*.35); conifer(110,z,.75+random.random()*.45)
# a few midground trees beyond site but not obstructing courtyard
for x,z in [(7,18),(8,76),(102,22),(100,78),(16,91),(90,92)]: conifer(x,z,.75+random.random()*.25)

# ---------- renderer ----------
ren=vtk.vtkRenderer(); ren.GradientBackgroundOn(); ren.SetBackground(.10,.14,.17); ren.SetBackground2(.40,.47,.49); ren.UseShadowsOff(); ren.UseSSAOOff(); ren.UseFXAAOff()
for a in actors: ren.AddActor(a)
# global lights
sun=vtk.vtkLight(); sun.SetLightTypeToSceneLight(); sun.SetPosition(-55,75,60); sun.SetFocalPoint(0,0,0); sun.SetColor(1,.72,.48); sun.SetIntensity(2.0); ren.AddLight(sun)
fill=vtk.vtkLight(); fill.SetLightTypeToSceneLight(); fill.SetPosition(55,45,-55); fill.SetFocalPoint(0,0,0); fill.SetColor(.52,.68,.82); fill.SetIntensity(.8); ren.AddLight(fill)
ambient=vtk.vtkLight(); ambient.SetLightTypeToSceneLight(); ambient.SetPosition(0,60,0); ambient.SetFocalPoint(0,0,0); ambient.SetColor(.75,.78,.75); ambient.SetIntensity(.55); ren.AddLight(ambient)
for l in lights: ren.AddLight(l)

win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.AddRenderer(ren); win.SetSize(1600,1000); win.SetMultiSamples(8)

cams={
1:([-4,16.79,1.28],[-4,2,33],44),
2:([-4,20.07,-5.99],[-4,2,28],45),
3:([23.83,29.46,-30.73],[-2,2,14],46),
4:([23.83,33.45,-33.83],[-18,2,8],48),
5:([25.99,35.14,-46.99],[-20,2,-1],48),
6:([32.65,42.80,-71.55],[0,2,-15],50),
7:([-8,28,-70],[-8,2,-15],58),
8:([-74,30,-8],[18,2,1],58),
}

def set_stage(stage):
    # stage-specific union deck: hide all exact deck actors except highest union applicable
    deck_exact=max([s for s in [2,4,6,7,8] if s<=stage], default=None)
    for a in actors:
        if hasattr(a,'_exact_deck_stage'):
            a.SetVisibility(a._exact_deck_stage==deck_exact)
        else:
            a.SetVisibility(a._stage<=stage)
    for l in lights: l.SetSwitch(1 if l._stage<=stage else 0)

def render_stage(stage):
    set_stage(stage)
    cam=vtk.vtkCamera(); pos,tgt,fov=cams[stage]; cam.SetPosition(*pos); cam.SetFocalPoint(*tgt); cam.SetViewUp(0,1,0); cam.SetViewAngle(fov); cam.SetClippingRange(.1,350); ren.SetActiveCamera(cam)
    win.Render()
    w2i=vtk.vtkWindowToImageFilter(); w2i.SetInput(win); w2i.SetScale(1); w2i.ReadFrontBufferOff(); w2i.Update()
    p=os.path.join(OUT,f'stage_{stage:02d}_hifi.png'); wr=vtk.vtkPNGWriter(); wr.SetFileName(p); wr.SetInputConnection(w2i.GetOutputPort()); wr.Write()
    # Match the display orientation of the accepted rough perspective views (mirrored east/west).
    im=Image.open(p).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    # subtle photographic grade
    im=ImageEnhance.Contrast(im).enhance(1.05); im=ImageEnhance.Color(im).enhance(.95); im=ImageEnhance.Brightness(im).enhance(.98)
    im.save(p)
    return p

if __name__=='__main__':
    paths=[render_stage(i) for i in range(1,9)]
    print('\n'.join(paths))
