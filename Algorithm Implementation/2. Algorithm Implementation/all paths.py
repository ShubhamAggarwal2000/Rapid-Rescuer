import numpy as np
def allpaths(graph):
    res=[]
    tmp=[]
    tmp.append(0)
    helper(res,graph,0,tmp)
    size = len(res)
    idx_list = [idx + 1 for idx, val in
            enumerate(res) if val == 0]
    idx_list=[x-1 for x in idx_list]
    idx_list.remove(0)
    res1 = [res[i: j] for i, j in
       zip([0] + idx_list, idx_list +
           ([size] if idx_list[-1] != size else []))]
    return res1
def helper(res,graph,cur,tmp):
    #print(cur)
    if (cur==len(graph)-1):
        res.extend(tmp)
        return
    for i in range(len(graph[cur])):
       # print(graph[cur][i])
        tmp.append(graph[cur][i])
        #print(tmp)
        helper(res,graph,graph[cur][i],tmp)
        tmp.pop()
graph=[[1,4],[2,3,4],[5,6,7],[4],[8],[],[],[4,8],[]]
allpaths(graph)
