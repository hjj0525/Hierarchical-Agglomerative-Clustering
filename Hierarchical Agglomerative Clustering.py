import math

def getCosSim(a, b):
    if(a==b):
        return -1
    
    dot = a[0] * b[0] + a[1] * b[1]
    norm = math.sqrt(a[0]**2+a[1]**2) * math.sqrt(b[0]**2+b[1]**2)
    
    return dot / norm


def hierarchy_clustering(fileName, link):

    f = open(fileName, 'r')
    info = f.readline()
    k, n = int(info.split()[0]), int(info.split()[1])
    
    dotList = []
    simList = []
    hierStack = []
    spanStack = []
    
    lines = f.readlines()
    
    # x,y 좌표값 리스트에 저장
    for line in lines:
        x, y =  int(line.split(',')[0]), int(line.split(',')[1])   
        dotList.append((x,y))
    
    simList = [[getCosSim(dotList[row], dotList[col]) for col in range(n)] for row in range(n)]
    
    f.close()
    
    while(len(simList) > 1):
        
        if(len(simList)==2):
            hierStack.append([dotList[0],dotList[1]])
            spanStack.append(simList[0][1])
            break;
          
        # 최대값 찾기
        rowMaxIdx = list(map(max,simList)).index(max(map(max,simList)))
        colMaxIdx = simList[rowMaxIdx].index(max(map(max,simList)))
        
        maxVal = simList[rowMaxIdx][colMaxIdx]
        
        newList=[]
        if(link == "single"):
            for row in range(len(simList)):
                simList[row].append(max(simList[row][rowMaxIdx], simList[row][colMaxIdx]))
                newList.append(max(simList[row][rowMaxIdx], simList[row][colMaxIdx]))
            newList.append(-1)
            simList.append(newList)
            
        elif(link == "complete"):
            for row in range(len(simList)):
                simList[row].append(min(simList[row][rowMaxIdx], simList[row][colMaxIdx]))
                newList.append(min(simList[row][rowMaxIdx], simList[row][colMaxIdx]))
            newList.append(-1)
            simList.append(newList)
        
        elif(link == "average"):
            for row in range(len(simList)):
                simList[row].append((simList[row][rowMaxIdx] + simList[row][colMaxIdx])/2)
                newList.append((simList[row][rowMaxIdx] + simList[row][colMaxIdx])/2)
            newList.append(-1)
            simList.append(newList)
            
            
        # 최대값 찾은 후 행,열 삭제
        # 각 2개씩 중복되므로 두 번씩 삭제, 하나 삭제 후 index 관리
        for row in range(len(simList)):
            del simList[row][rowMaxIdx]
        for row in range(len(simList)):
            del simList[row][colMaxIdx-1]
        del simList[rowMaxIdx]
        del simList[colMaxIdx-1]
        
        
        hierStack.append([dotList[rowMaxIdx],dotList[colMaxIdx]])
        spanStack.append(maxVal)
        # dotList도 조정
        dotList.append([dotList[rowMaxIdx], dotList[colMaxIdx]])    
        del dotList[rowMaxIdx]
        del dotList[colMaxIdx-1]
    
    hierStack.reverse()
    
    ## Tree 순회, Clustering ##
    first = hierStack[0][0]
    second = hierStack[0][1][0]
    third = hierStack[0][1][1]
        
        
    # Fir, Sec, Thi, String으로 변환 후 변경
    first = str(first).replace('[','').replace(']','')
    second = str(second).replace('[','').replace(']','')
    third = str(third).replace('[','').replace(']','')    
    
    # 출력부
    f2 = open(fileName[:-4]+"_output.txt", 'a')
    f2.writelines('---\n')
    f2.writelines(link+'\n')    
    f2.writelines('clusters: ['+first+'], ['+second+'], ['+third+']\n')
    f2.writelines("span: "+ str(spanStack[-3])+ ', '+ str(spanStack[-2])+'\n')
    f2.close()
    
if __name__ == "__main__":
    print("Insert a file name in the same folder")
    fileName = input()
    hierarchy_clustering(fileName, "single")
    hierarchy_clustering(fileName, "complete")
    hierarchy_clustering(fileName, "average")
   