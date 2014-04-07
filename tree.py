#!/usr/bin/env python
import sys, os

def getNodeList(dirName, flagList, layer, recur):
    layer += 1
    try:
        dirList = os.listdir(dirName)
        for node in dirList:
            flagList.append(layer)
            yield node
            if os.path.isdir(dirName + '/' + node) and layer < recur:
                for each in getNodeList(dirName + '/' + node, flagList, layer, recur):
                    yield each
    except OSError:
        yield dirName

def generateTree(nodeList, flag):
    prefix = "  |"
    layer = "    "
    trunk = "|"
    curLayer = 1
    for i in range(len(nodeList)):
        if flag[i] > curLayer:
            prefix = prefix + layer + trunk
        elif flag[i] < curLayer:
            while flag[i] != curLayer:
                prefix = prefix[0:2] + prefix[7:]
                curLayer -= 1
        curLayer = flag[i]
        print "%s---%s" % (prefix, nodeList[i])

def checkParameters(argv):
    if len(argv) < 2 or len(argv) > 3:
        print "Invalid parameter(s)! Parameter one should be an directory, parameter two should be an positive integer which is optional indicates that layers of sub directories you want to be displayed."
        print "Usage: tree {dir} [layer]"
        print "e.g. tree /root 2"
        return False
    else:
        if not os.path.isdir(argv[1]):
            print "No such directory named %s, you must input a valid directory name!" % argv[1]
            return False
        if len(argv) == 3:
            try:
                layers = int(argv[2])
                layers += 0
                if layers < 1:
                    raise ValueError
            except ValueError:
                print "You must input a positive integer as layers you wanted!"
                return False
    return True

if __name__ == '__main__':
    if checkParameters(sys.argv):
        lay = 6                          #By default, display 6 layers at most
        if len(sys.argv) == 3:
            lay = int(sys.argv[2])
        flag = []
        nodeList = list(getNodeList(sys.argv[1], flag, 0, lay))
        print os.path.basename(sys.argv[1])
        generateTree(nodeList, flag)
