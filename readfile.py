from pprint import pprint
import networkx as nx
def form_graph():
    G=nx.DiGraph()
    G=nx.read_gml("./test.gml")
    return G
    


def readFile():
    f = open('./test.csv', 'r')

    content = f.read()

    result = []

    big_lists = content.split(',')
    for big_list in big_lists:
        #result.append(list[int]())
        small_lists = big_list[1:-1].split(' ')
        small_list=(int(small_lists[0]),int(small_lists[1]))
        result.append(small_list)

    pprint(result)
    return result
#[1 2],[2 3]


def read_File(file):
    f = open(file, 'r')

    content = f.read()

    result = list[list[int]]()

    big_lists = content.split(',')
    for big_list in big_lists:
        result.append(list[int]())
        small_lists = big_list[1:-1].split(' ')
        for small_list in small_lists:
            result[-1].append(int(small_list))

    pprint(result)
    return result

def main():
    print('')
    #readFile()
    form_graph()
    
if __name__=="__main__":
    main()