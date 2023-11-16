import Kosaraju
import Tarjan
import Tarjan_Djikstra


def read_input_file():
    return

def kosaraju(inter,g):
    k=Kosaraju.KosarajuAlgorithm(g,inter)
    k.interface.write_to_log("INFO:   FIRST DFS IN ORDER TO PREPARE THE STACK FOR THE SECOND DFS")
    k.dfs(k.interface.first_node)
    k.interface.write_to_log("INFO:   TRANSPONING THE GRAPH FOR THE SECOND DFS")
    k.transpone_graph()
    k.reset_keys()
    k.interface.write_to_log("INFO:   SECOND DFS IN ORDER TO FIND ALL THE SCCS")
    k.transponed_dfs()
    k.interface.write_to_log("INFO:   NOW THAT WE HAVE FIND ALL SCCS ITS TIME TO RETURN THE ORIGINAL GRAPH")
    k.transpone_graph()
    k.interface.events()
    
def tarjan(inter,g):
    t=Tarjan.TarjanAlgorithm(g,inter)
    t.find_SCC(t.interface.first_node)
    t.interface.events()

def tarjan_djikstra(inter,g):
    inter.show_stack_P=True
    t=Tarjan_Djikstra.Tarjan_DjikstraAlgorithm(g,inter)
    t.find_SCSS(t.interface.first_node)
    t.write_SCC()
    t.interface.events()
    inter.show_stack_P=False
    return