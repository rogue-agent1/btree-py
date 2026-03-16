#!/usr/bin/env python3
"""B-Tree implementation with insert, search, and traversal."""
import sys

class BTreeNode:
    def __init__(self,t,leaf=True):
        self.t=t;self.leaf=leaf;self.keys=[];self.children=[]

class BTree:
    def __init__(self,t=2):self.t=t;self.root=BTreeNode(t)
    def search(self,key,node=None):
        if node is None:node=self.root
        i=0
        while i<len(node.keys) and key>node.keys[i]:i+=1
        if i<len(node.keys) and node.keys[i]==key:return True
        if node.leaf:return False
        return self.search(key,node.children[i])
    def insert(self,key):
        r=self.root
        if len(r.keys)==2*self.t-1:
            s=BTreeNode(self.t,False);s.children=[r]
            self._split(s,0);self.root=s
        self._insert_nonfull(self.root,key)
    def _split(self,parent,i):
        t=self.t;y=parent.children[i];z=BTreeNode(t,y.leaf)
        parent.keys.insert(i,y.keys[t-1])
        parent.children.insert(i+1,z)
        z.keys=y.keys[t:];y.keys=y.keys[:t-1]
        if not y.leaf:z.children=y.children[t:];y.children=y.children[:t]
    def _insert_nonfull(self,node,key):
        i=len(node.keys)-1
        if node.leaf:
            node.keys.append(0);
            while i>=0 and key<node.keys[i]:node.keys[i+1]=node.keys[i];i-=1
            node.keys[i+1]=key
        else:
            while i>=0 and key<node.keys[i]:i-=1
            i+=1
            if len(node.children[i].keys)==2*self.t-1:
                self._split(node,i)
                if key>node.keys[i]:i+=1
            self._insert_nonfull(node.children[i],key)
    def inorder(self,node=None):
        if node is None:node=self.root
        result=[]
        for i in range(len(node.keys)):
            if not node.leaf:result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])
        if not node.leaf:result.extend(self.inorder(node.children[-1]))
        return result

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        bt=BTree(2)
        for x in [10,20,5,6,12,30,7,17]:bt.insert(x)
        assert bt.search(6) and bt.search(30) and not bt.search(99)
        assert bt.inorder()==sorted([10,20,5,6,12,30,7,17])
        # Large insert
        bt2=BTree(3)
        for i in range(100):bt2.insert(i)
        assert bt2.inorder()==list(range(100))
        assert all(bt2.search(i) for i in range(100))
        assert not bt2.search(100)
        print("All tests passed!")
    else:
        bt=BTree(2)
        for x in [3,7,1,5,9,2,8,4,6]:bt.insert(x)
        print(f"Inorder: {bt.inorder()}")
if __name__=="__main__":main()
