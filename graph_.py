import pygame
import math
from button import *
import run_alg
import tkinter as tk
from tkinter import filedialog
import networkx as nx
from readfile import form_graph
import copy as c
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

TRANSPARENT_COLOR=(0,0,0,0)
fade_speed=30
line_color=(127,127,127)

class GraphInterface:
    display_width = 800
    display_height = 600
    stack_width=200
    stack=None
    screen = pygame.display.set_mode((display_width,display_height))
    pos_of_nodes={}
    radius=30
    font=None
    
    
    surfaces=[]
    current_surface=0
    num_of_surfaces=0
    surfaces_step_by_step={}
    logs=[]
    logs_step_by_step={}
    possible_start_nodes=[]
    
    
    run=True
    background_image = pygame.image.load("graph.jpg")
    colors_of_nodes={}
    graph=nx.DiGraph()
    message_log=[]
    stack_content=[]
    curr_message=0
    show_stack_P=False
    stack_P=None
    stack_P_content=[]
    first_node=0
    
    
    
    log_height=100
    log_position=0
    scroll_inc=0
    log=None
    
    control_window_width=200
    control_window=None
    play_button=Button(20,10,160,30,"PLAY",20,"crimson","darkred","white")
    pause_button=Button(20,50,160,30,"PAUSE",20,"crimson","darkred","white")
    prev_button=Button(20,90,70,30,"<-",20,"crimson","darkred","white")
    next_button=Button(110,90,70,30,"->",20,"crimson","darkred","white")
    slow_down_button=Button(20,140,70,30,"-",20,"crimson","darkred","white")
    speed_up_button=Button(110,140,70,30,"+",20,"crimson","darkred","white")
    back_button=Button(20,190,70,30,"BACK",20,"crimson","darkred","white")
    reset_button=Button(110,190,70,30,"RESET",20,"crimson","darkred","white")
    play=False
    current_step=0
    speed=1
    
    
    scroll_pos=0
    scroll_rect_pos=((display_width+stack_width*(2 if show_stack_P else 1)+control_window_width)-30,display_height,30,log_height)
    pooos=((display_width+stack_width*(2 if show_stack_P else 1)+control_window_width)-20,0,20,log_height)
    scroll_rect=pygame.Rect(pooos)
    scroll_x = 5
    scroll_y = 0
    scroll_button_width=20
    scroll_button = Button(scroll_x,scroll_y,scroll_button_width,30,"",20,"grey","lightgrey","white")
    
    selection_start=None
    selection_end=None
    mouse_button_down=False
    
    @classmethod
    def __init__(self):
        self.pos_of_nodes={}
        self.surfaces=[]
        self.current_surface=0
        self.num_of_surfaces=0
        self.surfaces_step_by_step={}
        self.run=True
        self.colors_of_nodes={}
        self.graph=nx.DiGraph()
        self.message_log=[]
        self.stack_content=[]
        self.curr_message=0
        self.show_stack_P=False
        self.stack_P_content=[]
        self.log_position=0
        
        self.play_button=Button(20,10,160,30,"PLAY",20,"crimson","darkred","white")
        self.pause_button=Button(20,50,160,30,"PAUSE",20,"crimson","darkred","white")
        self.prev_button=Button(20,90,70,30,"<-",20,"crimson","darkred","white")
        self.next_button=Button(110,90,70,30,"->",20,"crimson","darkred","white")
        self.slow_down_button=Button(20,140,70,30,"-",20,"crimson","darkred","white")
        self.speed_up_button=Button(110,140,70,30,"+",20,"crimson","darkred","white")
        self.back_button=Button(20,190,70,30,"BACK",20,"crimson","darkred","white")
        self.reset_button=Button(110,190,70,30,"RESET",20,"crimson","darkred","white")
        self.play=False
        self.current_step=0
        self.speed=1
        
        self.logs=[]
        self.logs_step_by_step={}
    
    @classmethod
    def redraw_base(self):
        self.screen.blit(pygame.image.load("blue.jpg"),(self.control_window_width,0))
        self.screen.blit(self.stack,(self.display_width+self.control_window_width,0))
        self.screen.blit(self.control_window,(0,0))
        self.init_control_window()
        if self.show_stack_P:
            self.screen.blit(self.stack_P,(self.display_width+self.stack_width+self.control_window_width,0))
            self.fill_stack_P()
        self.fill_stack()
        self.screen.blit(self.log,(0,self.display_height))
        #self.add_edges()
        
    @classmethod
    def add_ranks(self,low_ranks:dict):
        for x in low_ranks.keys():
            pos_of_x=(int(self.pos_of_nodes[x][0]*350+550),int(self.pos_of_nodes[x][1]*250+250))
            font = pygame.font.SysFont("Ink Free",18)
            text=font.render("{"+str(low_ranks[x])+"}",True,(255,255,255))
            self.screen.blit(text,(pos_of_x[0]-self.radius*2,pos_of_x[1]-self.radius*2))
        elem_surface=pygame.Surface((self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.display_height+self.log_height))
        elem_surface.blit(pygame.display.get_surface(),(0,0))
        self.surfaces_step_by_step[self.num_of_surfaces-1][-1]=(elem_surface)
       
    
    @classmethod
    def add_ranks_except(self,low_ranks:dict,skip):
        for x in low_ranks.keys():
            if x!=skip:
                pos_of_x=(int(self.pos_of_nodes[x][0]*350+550),int(self.pos_of_nodes[x][1]*250+250))
                font = pygame.font.SysFont("Arial",18)
                text=font.render("{"+str(low_ranks[x])+"}",True,(255,255,255))
                self.screen.blit(text,(pos_of_x[0]-self.radius*2,pos_of_x[1]-self.radius*2))
         
    @classmethod
    def add_error(self,msg,i):
            font = pygame.font.SysFont("Sans Serif",15)
            error=font.render(msg,True,'red')
            rect=error.get_rect()
            rect.bottomleft=(0,self.log_height-15*(i-1-self.scroll_inc))
            self.log.blit(error,rect)
            
            if self.selection_start is not None and self.selection_end is not None:
                if self.selection_start<=(i-1-self.scroll_inc)<=self.selection_end:
                    pygame.draw.rect(self.log,(0,0,255),(0,self.log_height-15*(i-self.scroll_inc),self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,15))
                    info=font.render(msg,True,'white')
                    rect=info.get_rect()
                    rect.bottomleft=(0,self.log_height-15*(i-1-self.scroll_inc))
                    self.log.blit(info,rect)
    
    @classmethod
    def add_message(self,msg,i):
            font = pygame.font.SysFont("Sans Serif",15)
            info=font.render(msg,True,'green')
            rect=info.get_rect()
            rect.bottomleft=(0,self.log_height-15*(i-1-self.scroll_inc))
            self.log.blit(info,rect)
            
            if self.selection_start is not None and self.selection_end is not None:
                if self.selection_start<=(i-1-self.scroll_inc)<=self.selection_end:
                    pygame.draw.rect(self.log,'blue',(0,self.log_height-15*(i-self.scroll_inc),self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,15))
                    info=font.render(msg,True,'white')
                    rect=info.get_rect()
                    rect.bottomleft=(0,self.log_height-15*(i-1-self.scroll_inc))
                    self.log.blit(info,rect)
            
    @classmethod
    def write_to_log(self,msg):
        self.message_log.append(msg)
        self.print_log()
        
        
    @classmethod
    def print_log(self):
        self.log.fill('black')
        for m in range(0,len(self.message_log)):
            if "INFO" in self.message_log[m]:
                self.add_message(self.message_log[m],len(self.message_log)-m)
            else:
                self.add_error(self.message_log[m],len(self.message_log)-m)
        self.screen.blit(self.log,(0,self.display_height))
            
            
    @classmethod
    def remember_surface(self):
        elem_surface=pygame.Surface((self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.display_height+self.log_height))
        elem_surface.blit(pygame.display.get_surface(),(0,0))
        self.surfaces.append(elem_surface)
        self.logs.append(c.copy(self.message_log))
        self.surfaces_step_by_step[self.num_of_surfaces]=[elem_surface]
        self.logs_step_by_step[self.num_of_surfaces]=[c.copy(self.message_log)]
        self.num_of_surfaces += 1
            
    @classmethod
    def part_of_surface(self):
        elem_surface=pygame.Surface((self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.display_height+self.log_height))
        elem_surface.blit(pygame.display.get_surface(),(0,0))
        self.surfaces_step_by_step[self.num_of_surfaces-1].append(elem_surface)
        self.logs_step_by_step[self.num_of_surfaces-1].append(c.copy(self.message_log))
   
    @classmethod
    def fade_in_text(self,low_ranks,i):
        R=0
        G=0
        B=0
        while R<225:
            self.redraw_base()
            
            R += 30
            G += 30
            B += 30
            self.add_edges()
            self.add_ranks_except(low_ranks,i)
            font = pygame.font.SysFont("Ink Free",18)
            text=font.render("{"+str(low_ranks[i])+"}",True,(R,G,B))
            pos_of_x=(int(self.pos_of_nodes[i][0]*350+550),int(self.pos_of_nodes[i][1]*250+250))
            self.screen.blit(text,(pos_of_x[0]-self.radius*2,pos_of_x[1]-self.radius*2))
            self.part_of_surface()
        
        
    @classmethod
    def fade_out_text(self,low_ranks,i):
        R=255
        G=255
        B=255
        while R>30:
            self.redraw_base()
            
            R -= 30
            G -= 30
            B -= 30
            self.add_edges()
            self.add_ranks_except(low_ranks,i)
            font = pygame.font.SysFont("Ink Free",18)
            text=font.render("{"+str(low_ranks[i])+"}",True,(R,G,B))
            pos_of_x=(int(self.pos_of_nodes[i][0]*350+550),int(self.pos_of_nodes[i][1]*250+250))
            self.screen.blit(text,(pos_of_x[0]-self.radius*2,pos_of_x[1]-self.radius*2))
            self.part_of_surface()
            
            
    @classmethod
    def push_on_stack(self,elem):
        start=10
        end=self.display_height-50*(len(self.stack_content)+1)
        while(start<=end-end/10):
            self.screen.blit(self.stack,(self.display_width+self.control_window_width,0))
            self.fill_stack()
            start+=end/10
            font = pygame.font.SysFont("Sans Serif",50)
            text=font.render(str(elem),True,'white')
            pygame.draw.rect(self.screen,'skyblue',(self.display_width+self.control_window_width+10,start,self.stack_width-20,40))
            self.screen.blit(text,(self.display_width+self.control_window_width+(self.stack_width-10)//2,start))
            self.part_of_surface()
        self.stack_content.append(elem)
     
     
    @classmethod   
    def pop_off_stack(self,elem):
        self.stack_content.pop()
        start=self.display_height-50*(len(self.stack_content)+1)
        end=self.display_height-50*(len(self.stack_content)+1)
        while(end!=0):
            self.screen.blit(self.stack,(self.display_width+self.control_window_width,0))
            self.fill_stack()
            end -=start/10
            font = pygame.font.SysFont("Sans Serif",50)
            text=font.render(str(elem),True,'white')
            pygame.draw.rect(self.screen,'skyblue',(self.display_width+self.control_window_width+10,end,self.stack_width-20,40))
            self.screen.blit(text,(self.display_width+self.control_window_width+(self.stack_width-10)//2,end))
            self.part_of_surface()
        self.part_of_surface()
        
        
    @classmethod
    def fill_stack(self):
        font = pygame.font.SysFont("Lucida Console",35)
        text=font.render("S T A C K",True,'skyblue')
        self.screen.blit(text,(self.display_width+self.control_window_width,10))
        for i in range(0,len(self.stack_content)):
            font = pygame.font.SysFont("Sans Serif",50)
            text=font.render(str(self.stack_content[i]),True,'white')
            pygame.draw.rect(self.screen,'skyblue',(self.display_width+self.control_window_width+10,self.display_height-50*(i+1),self.stack_width-20,40))
            self.screen.blit(text,(self.display_width+self.control_window_width+(self.stack_width-10)//2,self.display_height-50*(i+1)))
            
            
    @classmethod
    def push_on_stack_P(self,elem):
        start=10
        end=self.display_height-50*(len(self.stack_P_content)+1)
        while(start<=end-end/10):
            self.screen.blit(self.stack_P,(self.display_width+self.stack_width+self.control_window_width,0))
            self.fill_stack_P()
            start+=end/10
            font = pygame.font.SysFont("Sans Serif",50)
            text=font.render(str(elem),True,'white')
            pygame.draw.rect(self.screen,'skyblue',(self.display_width+self.control_window_width+self.stack_width+10,start,self.stack_width-20,40))
            self.screen.blit(text,(self.display_width+self.control_window_width+self.stack_width+(self.stack_width-10)//2,start))
            self.part_of_surface()
        self.stack_P_content.append(elem)
     
     
    @classmethod   
    def pop_off_stack_P(self,elem):
        self.stack_P_content.pop()
        start=self.display_height-50*(len(self.stack_P_content)+1)
        end=self.display_height-50*(len(self.stack_P_content)+1)
        while(end!=0):
            self.screen.blit(self.stack_P,(self.display_width+self.stack_width+self.control_window_width,0))
            self.fill_stack_P()
            end -=start/10
            font = pygame.font.SysFont("Sans Serif",50)
            text=font.render(str(elem),True,'white')
            pygame.draw.rect(self.screen,'skyblue',(self.display_width+self.control_window_width+self.stack_width+10,end,self.stack_width-20,40))
            self.screen.blit(text,(self.display_width+self.control_window_width+self.stack_width+(self.stack_width-10)//2,end))
            self.part_of_surface()
        self.part_of_surface()
        
    @classmethod
    def fill_stack_P(self):
        font = pygame.font.SysFont("Lucida Console",35)
        text=font.render("F R E E",True,'skyblue')
        self.screen.blit(text,(self.display_width+self.control_window_width+self.stack_width+20,10))
        for i in range(0,len(self.stack_P_content)):
            font = pygame.font.SysFont("Sans Serif",50)
            text=font.render(str(self.stack_P_content[i]),True,'white')
            pygame.draw.rect(self.screen,'skyblue',(self.display_width+self.control_window_width+self.stack_width+10,self.display_height-50*(i+1),self.stack_width-20,40))
            self.screen.blit(text,(self.display_width+self.control_window_width+self.stack_width+(self.stack_width-10)//2,self.display_height-50*(i+1)))
           
    

    @classmethod
    def draw_line(self,start_node,end_node,offset):
        
        angle=math.atan2(end_node[1]-start_node[1], end_node[0]-start_node[0])
        line_length = math.sqrt((end_node[0]-start_node[0])**2 + (end_node[1]-start_node[1])**2)
        if offset==0:
            
            end_x = (start_node[0]  + (line_length-self.radius)*math.cos(angle),start_node[1] + (line_length-self.radius)*math.sin(angle))
        else:
            offset_x=offset*math.sin(angle)
            offset_y=offset*math.cos(angle)
            
            start_node=(start_node[0],start_node[1])
            end_x = (start_node[0]  + (line_length-self.radius)*math.cos(angle),start_node[1]+offset + (line_length-self.radius)*math.sin(angle))
        
        pygame.draw.line(self.screen,line_color,(start_node[0]+offset,start_node[1]),end_x,2)     
        
        arrow_length=10
        arrow_angle = math.pi/6
        arrow_x = end_x[0]- arrow_length*math.cos(angle-arrow_angle)
        arrow_y = end_x[1] - arrow_length*math.sin(angle-arrow_angle)   
        pygame.draw.polygon(self.screen,line_color,[end_x,(arrow_x,arrow_y), (end_x[0]- arrow_length*math.cos(angle+arrow_angle),  end_x[1] - arrow_length*math.sin(angle+arrow_angle)  )])
             
    @classmethod
    def set_pos_of_nodes(self):
        self.pos_of_nodes=nx.spring_layout(self.graph,scale=0.8)
        for node in self.graph.nodes:
            self.colors_of_nodes[node]="aquamarine2"
                    
    @classmethod
    def add_text(self,node):
            pos_of_x=(int(self.pos_of_nodes[node][0]*350+550),int(self.pos_of_nodes[node][1]*250+250))
            font = pygame.font.SysFont("Ink Free",18)
            text=font.render(str(node),True,(0,0,0))
            self.screen.blit(text,(pos_of_x[0]-self.radius//4,pos_of_x[1]-self.radius//4))
    
    
           
            
    @classmethod
    def redraw_circles(self):
        self.redraw_base()
        for node in self.graph.nodes:
            pos_of_x=(int(self.pos_of_nodes[node][0]*350+550),int(self.pos_of_nodes[node][1]*250+250))
            pygame.draw.circle(self.screen,self.colors_of_nodes[node],pos_of_x,self.radius)
            self.add_text(node)
            
            
            
    @classmethod
    def change_color_of_node(self,node,color,inc):
        self.remember_surface()
        
        self.colors_of_nodes[node]=color
        self.redraw_base()
        self.add_edges()
        pos_of_x=(int(self.pos_of_nodes[node][0]*350+550),int(self.pos_of_nodes[node][1]*250+250))
        pygame.draw.circle(self.screen,self.colors_of_nodes[node],pos_of_x,self.radius+inc)
        self.add_text(node)
        self.part_of_surface()      
            
    @classmethod
    def remove_edges_with_fade(self):
        R=127
        G=127
        B=127
        while R>54:
            self.redraw_base()
            self.add_edges()
            
            R -=12
            G -= 12
            B -= 12

            for (x,y) in self.graph.edges:
                #print(x,y)
                
                x_coordinates =(int(self.pos_of_nodes[x][0]*350+550),int(self.pos_of_nodes[x][1]*250+250))
                y_coordinates =(int(self.pos_of_nodes[y][0]*350+550),int(self.pos_of_nodes[y][1]*250+250))
                if self.graph.has_edge(y,x):
                        if x<y:
                            self.faded_line(x_coordinates,y_coordinates,-15,(R,G,B)) 
                        else:
                            self.faded_line(x_coordinates,y_coordinates,15,(R,G,B)) 
                else:       
                        self.faded_line(x_coordinates,y_coordinates,0,(R,G,B)) 
                pygame.draw.circle(self.screen,self.colors_of_nodes[x],x_coordinates,self.radius)
                pygame.draw.circle(self.screen,self.colors_of_nodes[y],y_coordinates,self.radius)
                self.add_text(x)
                self.add_text(y)
            self.part_of_surface()
        self.redraw_circles()
                
    @classmethod
    def add_edges_with_fade(self):
        R=54
        G=54
        B=54
        while R<127:
            self.redraw_base()
            self.add_edges()
            
            R += 12
            G += 12
            B += 12
            
            # Calculate the color with the updated alpha value
            for (x,y) in self.graph.edges:
                x_coordinates =(int(self.pos_of_nodes[x][0]*350+550),int(self.pos_of_nodes[x][1]*250+250))
                y_coordinates =(int(self.pos_of_nodes[y][0]*350+550),int(self.pos_of_nodes[y][1]*250+250))
                if self.graph.has_edge(y,x):
                        if x<y:
                            self.faded_line(x_coordinates,y_coordinates,-15,(R,G,B)) 
                        else:
                            self.faded_line(x_coordinates,y_coordinates,15,(R,G,B)) 
                else:       
                        self.faded_line(x_coordinates,y_coordinates,0,(R,G,B)) 
                pygame.draw.circle(self.screen,self.colors_of_nodes[x],x_coordinates,self.radius)
                pygame.draw.circle(self.screen,self.colors_of_nodes[y],y_coordinates,self.radius)
                self.add_text(x)
                self.add_text(y)
            self.part_of_surface()
            
    
    @classmethod
    def faded_line(self,start_node,end_node,offset,color):
        angle=math.atan2(end_node[1]-start_node[1], end_node[0]-start_node[0])
        line_length = math.sqrt((end_node[0]-start_node[0])**2 + (end_node[1]-start_node[1])**2)
        if offset==0:
            
            end_x = (start_node[0]  + (line_length-self.radius)*math.cos(angle),start_node[1] + (line_length-self.radius)*math.sin(angle))
        else:
            offset_x=offset*math.sin(angle)
            offset_y=offset*math.cos(angle)
            
            start_node=(start_node[0],start_node[1])
            end_x = (start_node[0]  + (line_length-self.radius)*math.cos(angle),start_node[1]+offset + (line_length-self.radius)*math.sin(angle))
        
        pygame.draw.line(self.screen,color,(start_node[0]+offset,start_node[1]),end_x,2)     
        
        arrow_length=10
        arrow_angle = math.pi/6
        arrow_x = end_x[0]- arrow_length*math.cos(angle-arrow_angle)
        arrow_y = end_x[1] - arrow_length*math.sin(angle-arrow_angle)   
        pygame.draw.polygon(self.screen,color,[end_x,(arrow_x,arrow_y), (end_x[0]- arrow_length*math.cos(angle+arrow_angle),  end_x[1] - arrow_length*math.sin(angle+arrow_angle)  )])
   

            
    @classmethod
    def add_edges(self):
        for (x,y) in self.graph.edges:
            #print(x,y)
            x_coordinates =(int(self.pos_of_nodes[x][0]*350+550),int(self.pos_of_nodes[x][1]*250+250))
            y_coordinates =(int(self.pos_of_nodes[y][0]*350+550),int(self.pos_of_nodes[y][1]*250+250))
            if self.graph.has_edge(y,x):
                    if x<y:
                        self.draw_line(x_coordinates,y_coordinates,-15) 
                    else:
                        self.draw_line(x_coordinates,y_coordinates,15) 
            else:       
                 self.draw_line(x_coordinates,y_coordinates,0) 
            pygame.draw.circle(self.screen,self.colors_of_nodes[x],x_coordinates,self.radius)
            pygame.draw.circle(self.screen,self.colors_of_nodes[y],y_coordinates,self.radius)
            self.add_text(x)
            self.add_text(y)
            
            
    @classmethod
    def start_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((self.display_width,self.display_height))
        screen.fill('grey')
        rect=self.background_image.get_rect()
        rect.center=self.display_width//3, self.display_height//3
        screen.blit(self.background_image,rect)
        
        
        pygame.display.update()
        
       
            
        font = pygame.font.SysFont("ebrima",80)
        text=font.render("Visualisation of SCSS",True,'black')
        shadow_text=font.render("Visualisation of SCSS",True,'skyblue')
        text_rect=text.get_rect(center=(400,100))
        self.screen.blit(text,text_rect)
        self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5))
        
        
        pygame.display.update()
        
        play_button=Button(250,250,250,100,"PLAY",40,"crimson","darkred","white")
        play_button.draw(self.screen)
        exit_button=Button(250,410,250,100,"EXIT",40,"crimson","darkred","white")
        exit_button.draw(self.screen)
        pygame.display.update()
        
        while self.run:
            events=pygame.event.get()
            for e in events:
                if e.type==pygame.QUIT:
                    self.run=False
                    break
                elif e.type==pygame.MOUSEMOTION:
                    pos=pygame.mouse.get_pos()
                    if pos[0]<self.display_width and pos[1]<self.display_height and pos[0]>0 and pos[1]>0:
                        rect.center=pos[0]//7, pos[1]//7
                        self.screen.blit(self.background_image,rect)
                       
                        self.screen.blit(text,text_rect)
                        self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5))
                        play_button.draw(self.screen)
                        exit_button.draw(self.screen)
                        
                    else:
                        rect.center= self.display_width//2,self.display_height//2
                        self.screen.blit(self.background_image,rect)
                       
            
                        self.screen.blit(text,text_rect)
                        self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5))
                        play_button.draw(self.screen)
                        exit_button.draw(self.screen)
                        
                    play_button.update()
                    play_button.draw(self.screen)
                    exit_button.update()
                    exit_button.draw(self.screen)
                    pygame.display.update()
                elif e.type==pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked():
                        self.pick_alg()
                        self.run=False
                        continue
                    elif exit_button.is_clicked():
                        self.run=False
                        continue
                    
        
        
    @classmethod
    def pick_csv(self):
        root=tk.Tk()
        root.withdraw()
        filepath=filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        return filepath
        
    @classmethod
    def pick_alg(self):
        screen = pygame.display.set_mode((self.display_width,self.display_height))
        rect=self.background_image.get_rect()
        rect.center=self.display_width//3, self.display_height//3
        screen.blit(self.background_image,rect)
        
        font = pygame.font.SysFont("ebrima",80)
        text=font.render("Pick an algorithm",True,'black')
        shadow_text=font.render("Pick an algorithm",True,'skyblue')
        text_rect=text.get_rect(center=(400,50))
        self.screen.blit(text,text_rect)
        self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5))
        
        first_alg_button=Button(210,150,360,100,"KOSARAJU",40,"crimson","darkred","white")
        first_alg_button.draw(self.screen)
        second_alg_button=Button(210,300,360,100,"TARJAN",40,"crimson","darkred","white")
        second_alg_button.draw(self.screen)
        third_alg_button=Button(210,450,360,100,"TARJAN/DJIKSTRA",40,"crimson","darkred","white")
        third_alg_button.draw(self.screen)
        
        pygame.display.update()
        
        picking=True
        
        while picking:
            events=pygame.event.get()
            
            for e in events:
                if e.type==pygame.MOUSEMOTION:
                    pos=pygame.mouse.get_pos()
                    if pos[0]<self.display_width and pos[1]<self.display_height and pos[0]>0 and pos[1]>self.log_height:
                    
                        rect.center=pos[0]//7, pos[1]//7
                        self.screen.blit(self.background_image,rect)
                        
                        self.screen.blit(text,text_rect)
                        self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5))
                       
                        first_alg_button.draw(self.screen)
                        second_alg_button.draw(self.screen)
                        third_alg_button.draw(self.screen)
                        
                    else:
                        rect.center= self.display_width//2,self.display_height//2
                        self.screen.blit(self.background_image,rect)
                       
                        self.screen.blit(text,text_rect)
                        self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5))
                        
                        
                        first_alg_button.draw(self.screen)
                        second_alg_button.draw(self.screen)
                        third_alg_button.draw(self.screen)
                     
                    self.screen.blit(text,text_rect)
                    self.screen.blit(shadow_text,(text_rect.x+5,text_rect.y+5)) 
                    
                    first_alg_button.update()
                    second_alg_button.update()
                    third_alg_button.update()
                    first_alg_button.draw(self.screen)
                    second_alg_button.draw(self.screen)
                    third_alg_button.draw(self.screen)   
                    pygame.display.update()
                
                if e.type==pygame.MOUSEBUTTONDOWN:
                    if first_alg_button.is_clicked():
                        self.graph=form_graph()
                        run_alg.kosaraju(self,self.graph)
                        picking=False
                        break
                    if second_alg_button.is_clicked():
                        self.tarjan=True
                        self.graph=form_graph()
                        
                        run_alg.tarjan(self,self.graph)
                        self.tarjan=False
                        picking=False
                        break
                    if third_alg_button.is_clicked():
                        self.show_stack_P=True
                        self.graph=form_graph()
                        
                        run_alg.tarjan_djikstra(self,self.graph)
                        picking=False
                        break
    
    
    @classmethod
    def set_Tarjan_Djikstra(self):
        self.show_stack_P=True
        
    @classmethod
    def change_graph(self,g):
        self.graph=self.graph.reverse()
    
    @classmethod
    def copy_graph(self,g):
        self.graph=g
        
        
    @classmethod
    def init_control_window(self):
        self.control_window=pygame.Surface((200,self.display_height))
        self.control_window.blit(pygame.image.load("sky.jpg"),(0,0))
        self.screen.blit(self.control_window,(0,0))
        self.play_button.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.prev_button.draw(self.screen)
        self.next_button.draw(self.screen)
        self.slow_down_button.draw(self.screen)
        self.speed_up_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        
    @classmethod
    def check_control_buttons(self,action):
        if action==pygame.MOUSEBUTTONDOWN:
            if(self.play_button.is_clicked()):
                self.play=True
            elif self.next_button.is_clicked():
                self.play=False
                self.next_surface()
            elif self.prev_button.is_clicked():
                self.play=False
                self.prev_surface()
            elif self.back_button.is_clicked():
                self.play=False
                self.pick_alg()
            elif self.reset_button.is_clicked():
                self.play=False
                self.screen.blit(self.surfaces[0],(0,0))
                self.current_surface=0
                
                pygame.display.flip()
            elif self.speed_up_button.is_clicked():
                self.speed-=0.2
            elif self.slow_down_button.is_clicked():
                self.speed+=0.2
            elif self.pause_button.is_clicked():
                self.play=False
            
        else:
            self.update_control_buttons()
            self.draw_control_buttons()
            pygame.display.update()
        
    
    @classmethod
    def update_control_buttons(self):
        self.play_button.update()
        self.pause_button.update()
        self.prev_button.update()
        self.next_button.update()
        self.back_button.update()
        self.reset_button.update()
        self.speed_up_button.update()
        self.slow_down_button.update()
        
    @classmethod
    def draw_control_buttons(self):
        self.play_button.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.prev_button.draw(self.screen)
        self.next_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.speed_up_button.draw(self.screen)
        self.slow_down_button.draw(self.screen)
    @classmethod
    def draw_graph(self):
       # self.graph=form_graph()
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.display_height+self.log_height))
        self.stack=pygame.Surface((self.stack_width,self.display_height))
        self.log=pygame.Surface((self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))
        self.stack.blit(pygame.image.load("sky.jpg"),(0,0))
        self.screen.fill('grey')
        self.screen.blit(pygame.image.load("blue.jpg"),(self.control_window_width,0))
        self.screen.blit(self.stack,(self.display_width+self.control_window_width,0))
        self.log.fill('black')
        self.screen.blit(self.log,(0,self.display_height))
        if self.show_stack_P:
            self.stack_P=pygame.Surface((self.stack_width,self.display_height))
            self.stack_P.blit(pygame.image.load("sky.jpg"),(0,0))
            self.screen.blit(self.stack_P,(self.display_width+self.stack_width+self.control_window_width,0))
            font = pygame.font.SysFont("Lucida Console",35)
            text=font.render("F R E E",True,'skyblue')
            self.screen.blit(text,(self.display_width+self.stack_width+220,10))
        self.init_control_window()
        font = pygame.font.SysFont("Lucida Console",35)
        text=font.render("S T A C K",True,'skyblue')
        self.screen.blit(text,(self.display_width+self.control_window_width,10))
        
        #pygame.display.update()               
        self.set_pos_of_nodes()
        self.add_start_node()
        self.check_if_good_start_node()
        self.add_edges()
        self.remember_surface()
        pygame.display.update()

    @classmethod 
    def check_if_good_start_node(self):
        pick_again=True
        font = pygame.font.SysFont("Sans Serif",40)
        error=font.render("PICK START NODE FOR DEPTH FIRST SEARCH (DFS)",True,'green1')
        rect=error.get_rect()
        rect.center=(self.control_window_width+self.display_width//2,self.display_height//2)
        self.screen.blit(error,rect)
        pygame.display.update()
        pygame.time.delay(500)
        self.redraw_base()
        self.add_edges()
        pygame.display.update()
        while pick_again:
            node_picked=False
            while node_picked==0:
                events=pygame.event.get()
                for e in events:
                    if(e.type==pygame.MOUSEBUTTONDOWN):
                        pos=pygame.mouse.get_pos()
                        for i in self.possible_start_nodes:
                            x_coordinates =(int(self.pos_of_nodes[i][0]*350+550),int(self.pos_of_nodes[i][1]*250+250))
                            if ((pos[0]-x_coordinates[0])**2 + (pos[1]-x_coordinates[1])**2)<=self.radius**2:
                                pick_again=False
                                self.first_node=i
                                for node in self.graph.nodes:
                                    self.colors_of_nodes[node]="aquamarine2"
                                self.redraw_base()
                                self.add_edges()
                                pygame.display.update()
                                return
        
        

    @classmethod
    def add_start_node(self):
        for node in self.graph.nodes:
            nodes_reached=[node]
            for edge in list(self.graph.edges):
                if edge[0] in nodes_reached and edge[1] not in nodes_reached:
                    nodes_reached.append(edge[1])
            if len(nodes_reached)==len(self.graph.nodes):
                self.possible_start_nodes.append(node)
        for node in self.graph.nodes:
            if node not in self.possible_start_nodes:
                self.colors_of_nodes[node]="grey"
        
    @classmethod
    def events(self):
        self.remember_surface()
        self.screen.blit(self.surfaces[0],(0,0))
        self.current_surface=0
        pygame.display.flip()
        while(self.run):
            events=pygame.event.get()
            for e in events:
                pos=pygame.mouse.get_pos()
                if pos[0]<self.control_window_width and pos[1]<self.display_height and pos[0]>0 and pos[1]>0:
                    self.check_control_buttons(e.type)
                if pos[0]<self.display_width and pos[1]<self.display_height+self.log_height and pos[0]>0 and pos[1]>self.display_height:
                   # self.log.blit() 
                    if e.type==pygame.MOUSEBUTTONDOWN:
                        if e.button==4:
                            if (len(self.message_log)+self.scroll_inc)>len(self.message_log):
                                print(self.log_height//15+self.log_height//(15*(self.log_height//15)))
                                print(self.scroll_inc)
                                self.scroll_inc -=1
                            
                            self.print_log()
                            pygame.display.update((0,self.display_height,self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))

                        elif e.button == 5:
                            if (len(self.message_log)-self.scroll_inc)>(self.log_height//15+self.log_height//(15*(self.log_height//15))):
                                self.scroll_inc += 1
                            self.print_log()
                            pygame.display.update((0,self.display_height,self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))
                        else:
                            if(self.mouse_button_down):
                                self.selection_end=None
                                self.selection_start=None
                                self.mouse_button_down=False
                                self.print_log()
                                pygame.display.update((0,self.display_height,self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))

                            self.selection_start=(self.log_height-pos[1]+self.display_height)//15
                            print(self.selection_start)
                            self.mouse_button_down=True
                            self.print_log()
                            pygame.display.update((0,self.display_height,self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))

                    elif e.type==pygame.MOUSEMOTION:
                        if self.mouse_button_down:
                            self.selection_end=(self.log_height-pos[1]+self.display_height)//15
                            self.print_log()
                            pygame.display.update((0,self.display_height,self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))
                    elif e.type==pygame.MOUSEBUTTONUP:
                        self.mouse_button_down=False
                if e.type==pygame.QUIT:
                    self.run=False
                    break
                
                
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_LEFT:
                        self.prev_surface()
                    if e.key==pygame.K_RIGHT:
                        self.next_surface()
                    elif e.key==pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        pygame.scrap.init()
                        selected_text = '\n'.join(self.message_log[self.selection_start:self.selection_end+1])
                        pygame.scrap.put(pygame.SCRAP_TEXT, selected_text.encode())
                        self.selection_start=None
                        self.selection_end=None
                        self.print_log()
                        pygame.display.update((0,self.display_height,self.display_width+self.stack_width*(2 if self.show_stack_P else 1)+self.control_window_width,self.log_height))

                        
            if self.play:
                    num_of_steps=len(self.surfaces_step_by_step[self.current_surface])
                    if self.current_step>(num_of_steps-1):
                        self.current_surface = self.current_surface + 1
                        if self.current_surface <= (len(self.surfaces_step_by_step)-1):
                            num_of_steps = len(self.surfaces_step_by_step[self.current_surface])
                            self.current_step = 0
                        else:
                            self.play=False
                            continue
                    self.screen.blit(self.surfaces_step_by_step[self.current_surface][self.current_step],(0,0))
                    self.message_log=self.logs_step_by_step[self.current_surface][self.current_step]
                    self.current_step=self.current_step+1
                    self.update_control_buttons()
                    self.draw_control_buttons()
                    pygame.display.flip()
                    pygame.time.delay(100+int(100*self.speed))
    @classmethod
    def prev_surface(self):
        if(self.current_surface>0):
            self.current_surface=self.current_surface-1
            self.screen.blit(self.surfaces[self.current_surface],(0,0))
            self.message_log=c.copy(self.logs[self.current_surface])
            pygame.display.flip()
    
    @classmethod
    def next_surface(self):
        if self.current_surface<len(self.surfaces)-1:
            
            self.current_surface=self.current_surface+1
            self.screen.blit(self.surfaces[self.current_surface],(0,0))
            self.message_log=c.copy(self.logs[self.current_surface])
            print(self.logs[self.current_surface])
            pygame.display.flip()
                
            
                        
def main():
    g=GraphInterface()
    
    g.start_screen()
    
if __name__=="__main__":
    main()