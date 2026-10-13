from math import *
from ion import *
from kandinsky import *
from random import *
from filter import *
from kandin import *
white=(255,255,255)
black=(10,10,10)
red=(255,0,0)
blue=(0,0,255)
green=(0,255,0)
brightnessCoef=300

def briefingEng():
  fill_rect(0,0,320,222,black)
  draw_string("FIELD OPERATIONS DIV.",5,5,(220,50,50),black)
  draw_string("BRIEFING 01 : SITE INSPECTION",5,20,white,black)
  draw_string("Investigate the loss of contact",5,35,white,black)
  draw_string("at Research Site 7. Recover its ",5,50,white,black)
  draw_string("data unit. The site was evacua-",5,65,white,black)
  draw_string("ted after an incident. In order",5,80,white,black)
  draw_string("to perform your task, you have ",5,95,white,black)
  draw_string("three sensors at your disposal:",5,110,white,black)
  draw_string("RED: Physical attributes",5,125,red,black)
  draw_string("GREEN: Structure & material",5,140,green,black)
  draw_string("BLUE: Facility records",5,155,blue,black)
  draw_string("Remain calm. Trust your tools.",5,170,white,black)
  draw_string("YOUR SAFETY IS OUR PRIORITY",5,185,white,black)
  draw_string("PRESS OK TO BEGIN",8,200,white,black)

def frame():
  fill_rect(0,0,320,222,(10,10,10))

def icon(x,y,col):
  rectadd(x,y-9,10,8,col[0],col[1],col[2])
  rectadd(x-9,y+6,10,8,col[0],col[1],col[2])
  rectadd(x+9,y+6,10,8,col[0],col[1],col[2])
  rectadd(x+1,y-10,8,10,col[0],col[1],col[2])
  rectadd(x-8,y+5,8,10,col[0],col[1],col[2])
  rectadd(x+10,y+5,8,10,col[0],col[1],col[2])

def deathscreen(i,text):
  y=randint(1,222)
  condition=randint(1,100)

  fill_rect(0,y,320,1,(i+randint(-i,i),i+randint(-i,i),i+randint(-i,i)))
  fill_rect(0,y,320,3,(10,10,10))
  fill_rect(randint(1,300),y,200,1,white)
  fill_rect(0,y,320,1,(i+randint(-i,i),i+randint(-i,i),i+randint(-i,i)))
  
  tx=160-(len(text)*5)
  if condition>94:
    fill_rect(0,0,320,222,black)
  elif condition==93:
    draw_string(text,tx+5,105,red,black)
  elif condition==92:
    draw_string(text,tx-5,100,green,black)
  elif condition==91:
    draw_string(text,tx+1,107,blue,black)
  else:
    draw_string(text,tx,100,white,black)
    icon(150,50,red)
    icon(152,50,green)
    icon(151,51,blue)

def motionFB():
  if keydown(KEY_UP):
    return moveSpd
  if keydown(KEY_DOWN):
    return -moveSpd
  return 0

def motionLR(orient,turnSpd):
  if keydown(KEY_LEFT):
    orient+=turnSpd
  if keydown(KEY_RIGHT):
    orient-=turnSpd
  return orient

def interact(obj,room):
  destinations={
    "to_entry":0,
    "to_hub":1,
    "to_admin":2,
    "to_labs":3
  }

  if obj.g=="door":
    if obj.b in destinations:
      newRoom=destinations[obj.b]
      return newRoom,"DOOR: TRANSIT INITIATED"

    return room,"ACCESS DENIED"

  if obj.b=="comp_unit":
    return room,"DATA UNIT: NO RESPONSE"

  if obj.b=="pickup?":
    return room,"UNKNOWN OBJECT ACQUIRED"

  return room,"NO INTERACTION AVAILABLE"    

def place(obj,x,y,tr,tg,tb,selectable=False):
  dx=obj.x-x
  dy=obj.y-y

  angle=orient*2*pi/700
  depth=dx*cos(angle)+dy*sin(angle)
  side=-dx*sin(angle)+dy*cos(angle)

  if depth<=50:
    selectable=True
  else:
    selectable=False
    
  if depth<=8:
    return

  focal=120
  horizon=110
  screenx=int(160-focal*side/depth)
  if screenx < 0 or screenx > 310:
    return

  screeny=int(horizon+72/depth)
  bright=min((1,brightnessCoef/(depth+12)))
  r=int(255*bright)
  g=int(255*bright)
  b=int(255*bright)
  
  if selectable:
    draw_string(obj.r,screenx,screeny-20,white,black)
    draw_string(obj.g,screenx,screeny,white,black)
    draw_string(obj.b,screenx,screeny+20,white,black)
  else:
    if tr:
      draw_string(obj.r,screenx,screeny-20,(r,0,0),black)
    if tg:
      draw_string(obj.g,screenx,screeny,(0,g,0),black)
    if tb:
      draw_string(obj.b,screenx,screeny+20,(0,0,b),black)

def findTarget(orient,x,y,objects):
  angle=orient*2*pi/700
  target=None
  nearest=50

  for obj in objects:
    dx=obj.x-x
    dy=obj.y-y

    depth=dx*cos(angle)+dy*sin(angle)
    side=-dx*sin(angle)+dy*cos(angle)

    if depth<=8 or depth>=nearest:
      continue

    screenx=160-120*side/depth

    if abs(screenx-160)<=30:
      target=obj
      nearest=depth
  return target

def livescreen(orient,x,y,objects,tr,tg,tb):
  visible=[]
  angle=orient*2*pi/700
  fill_rect(0,50,320,122,black)

  target=findTarget(orient,x,y,objects)
  
  for obj in objects:
    dx=obj.x-x
    dy=obj.y-y
    depth=dx*cos(angle)+dy*sin(angle)
    visible.append((depth,obj))

  visible.sort(reverse=True,key=lambda item: item[0])

  for depth,obj in visible:
    place(obj,x,y,tr,tg,tb,obj is target)

  return target

class Entity():
  def __init__(self,r,g,b,x,y):
    self.r=r
    self.g=g
    self.b=b
    self.x=x
    self.y=y

def UItop(tr,tg,tb):
  fill_rect(0,0,320,50,(0,0,0))
  if tr:
    icon(20,20,red)
    draw_string("7",60,15,red,(0,0,0))
  if tg:
    icon(22,20,green)
    draw_string("8",80,14,green,(0,0,0))
  if tb:
    icon(21,21,blue)
    draw_string("9",100,14,blue,(0,0,0))

def UIbottom(orient):
  fill_rect(0,172,320,50,(0,0,0))
  for n in range(7):
    fill_rect((orient-100)%700-2,180,6,4,(250,200,20))
    fill_rect((orient-100)%700-1,179,4,6,(250,200,20))
    fill_rect((orient-100*n)%700,190,2,20,white)
    fill_rect((orient-100*n)%700-50,200,2,10,(100,100,100))
    fill_rect((orient-100*n)%700-25,205,2,5,(50,50,50))
    fill_rect((orient-100*n)%700-75,205,2,5,(50,50,50))

def create(list,indx):
  entry=[["cold","metal","table",550,150],
  ["dusty","box","comp_unit",650,150],
  ["solid","door","to_hub",-150,700],
  ["solid","vertical","pole_E1",500,500],
  ["solid","vertical","pole_E2",500,-500],
  ["solid","vertical","pole_E3",-500,500],
  ["solid","vertical","pole_E4",-500,-500]]
  hub=[["solid","door","to_entry",-150,700],
  ["solid","door","[sealed]",-700,0],
  ["solid","door","to_labs",0,700],
  ["solid","door","to_admin",0,-700],
  ["white","flat","public",500,-700],
  ["broken","abstract","pickup?",20,50],
  ["cold","lump","obsolete_equipment",-700,-500]]
  admin=[["solid","door","to_hub",0,-700],
  ["solid","box","locker_A1",-300,-600],
  ["solid","box","locker_A2",-300,-400],
  ["solid","box","locker_A3",-300,-200],
  ["solid","box","locker_A4",-300,0]]
  r4=[]
  rooms=[entry,hub,admin,r4]
  room=rooms[indx]
  for i in range(len(room)):
    list.append(Entity(room[i][0],room[i][1],room[i][2],room[i][3],room[i][4]))

on=False
frame()
orient=50
x=0.0
y=0.0
moveSpd=4
turnSpd=2
tr=tg=tb=True
objects=[]

message=""
ok_was_down=False
target=None

room=0
create(objects,room)

briefingEng()
while not on:
  if keydown(KEY_OK):
    on=True
    sleep(1)

UItop(tr,tg,tb)
UIbottom(orient)

while on:
  orient=motionLR(orient,turnSpd)%700
  d=motionFB()
  angle=orient*2*pi/700
  x+=d*cos(angle)
  y+=d*sin(angle)
  
  target = livescreen(orient,x,y,objects,tr,tg,tb)
  UIbottom(orient)

  ok_down=keydown(KEY_OK)
  if ok_down and not ok_was_down and target is not None:
    oldRoom=room
    ok_was_down=True
    room=interact(target,room)[0]
    message=interact(target,room)[1]
    objects=[]
    create(objects,room)
    frame()
    for n in range(30):
      deathscreen(10,message)
    UItop(tr,tg,tb)
  ok_was_down=False
  
  if keydown(KEY_EIGHT):
    tg=not tg
    UItop(tr,tg,tb)
    sleep(0.2)
  if keydown(KEY_SEVEN):
    tr=not tr
    UItop(tr,tg,tb)
    sleep(0.2)
  if keydown(KEY_NINE):
    tb=not tb
    UItop(tr,tg,tb)
    sleep(0.2)
    
  if keydown(KEY_VAR):
    on=False
    fill_rect(0,0,320,222,black)
  if keydown(KEY_SHIFT):
    blurV(1)

  #Debug 2D top-down
  if keydown(KEY_ALPHA):
    fill_rect(150+int(x/20),100+int(y/20),5,5,white)
    for obj in objects:
      draw_string(obj.r,150+int(obj.x/20),100+int(obj.y/20),red)
  if keydown(KEY_XNT):
    fill_rect(150+int(x/20),100+int(y/20),5,5,white)
    for obj in objects:
      fill_rect(150+int(obj.x/20),100+int(obj.y/20),5,5,red)
while not on:
  deathscreen(10,"no_signal")
