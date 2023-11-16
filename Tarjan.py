
#impl i prikaz ranka
import graph_
import random
import copy
import networkx as nx

class TarjanAlgorithm:

    stack=[]
    visited={}
    graph=nx.DiGraph()
    low_rank={}
    interface=graph_.GraphInterface()
    found_scc=[]    
    g=0
    b=0

    def __init__(self,grap:nx.DiGraph,interface):
        for i in grap.nodes:
            self.visited[i]=False
            self.low_rank[i]=i
            print(self.low_rank)
        self.interface=graph_.GraphInterface()
        self.interface.copy_graph(grap)
        self.interface.draw_graph()
        self.interface.add_ranks(self.low_rank)
    
    @classmethod
    def dfs(self,node):
        self.visited[node]=True
        self.interface.push_on_stack(node)
        self.stack.append(node)
        self.interface.change_color_of_node(node,"aquamarine2",5)
        self.interface.add_ranks(self.low_rank)
        for edge in list(self.interface.graph.neighbors(node)):
                if not self.visited[edge]:
                    self.interface.write_to_log("INFO:   VISITING NODE "+str(edge)+" FROM NODE "+str(node))
                    self.dfs(edge)
                else:
                    self.interface.write_to_log("ERROR:   CANNOT VISIT NODE "+str(edge)+" SINCE IT IS ALREADY VISITED")
                    
                if self.stack.count(edge)>0:
                    prev_rank=self.low_rank[node]
                    self.low_rank[node]=min(self.low_rank[node],self.low_rank[edge])
                    if prev_rank!=self.low_rank[node]:
                        low_ranks_copy=copy.deepcopy(self.low_rank)
                        low_ranks_copy[node]=prev_rank
                        self.interface.write_to_log("INFO:   CHANGING LOWEST RANK FOR NODE "+str(node)+" TO LOWEST RANK OF NODE "+str(edge))
                        self.interface.fade_out_text(low_ranks_copy,node)
                        self.interface.fade_in_text(self.low_rank,node)
                
        if node==self.low_rank[node]:
            curr_scc=[]
            r=random.randint(200,255)
            self.g=(self.g+60)%256
            self.b=(self.b+60)%256
            while len(self.stack)>0:
                n=self.stack.pop()
                self.interface.pop_off_stack(n)
                prev_rank=self.low_rank[n]
                self.low_rank[n]=node
                curr_scc.append(n)
                self.interface.change_color_of_node(n,(r,self.g,self.b),5)
                self.interface.add_ranks(self.low_rank)
                if prev_rank!=self.low_rank[n]:
                    low_ranks_copy=copy.deepcopy(self.low_rank)
                    low_ranks_copy[n]=prev_rank
                    self.interface.write_to_log("INFO:   CHANGING LOWEST RANK FOR NODE "+str(n)+" TO LOWEST RANK OF NODE "+str(node))
                    
                    self.interface.fade_out_text(low_ranks_copy,n)
                    self.interface.fade_in_text(self.low_rank,n)
                self.interface.change_color_of_node(n,(r,self.g,self.b),0)
                self.interface.add_ranks(self.low_rank)
                if n==node:
                    break
            self.found_scc.append(curr_scc)
                
                
    
    @classmethod
    def find_SCC(self,node):
        for edge in list(self.interface.graph.neighbors(node)):
            if  not self.visited[edge]:
                self.dfs(node)
        self.interface.add_ranks(self.low_rank)
        self.interface.write_to_log("INFO: THE FOUND SCCS ARE:")
        for scc in self.found_scc:
            text=""
            for node in scc:
                text+=str(node)+" "
            self.interface.write_to_log("INFO:"+text)
    