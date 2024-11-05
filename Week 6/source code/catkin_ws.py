#!/usr/bin/env python3
import matplotlib.pyplot as plt
import rospy
import numpy as np
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, x, y, node_id):
        self.point = Point(x, y)
        self.node_id = node_id
        self.neighbors = []

class PRM:
    def __init__(self, x_max, x_min, y_max, y_min, numNodes):
        self.x_max = x_max
        self.y_max = y_max
        self.x_min = x_min
        self.y_min = y_min
        self.numNodes = numNodes
        self.nodes = []
        self.nodes.append(Node(0, 0, 0))  # Start node
        self.nodes.append(Node(18, 18, 1))  # Goal node
    
    def generateRandomPoints(self, obsVec):
        total = 0
        while total < self.numNodes:
            p = Node(np.random.uniform(self.x_min, self.x_max),
                      np.random.uniform(self.y_min, self.y_max),
                      total + 2)
            if not self.intersects0bs(p.point, p.point, obsVec) and self.isWithinWorld(p.point):
                self.nodes.append(p)
                total += 1

    def computeNeighborGraph(self, obsVec):
        for i in self.nodes:
            distanceMap = []
            for j in self.nodes:
                if i.node_id != j.node_id and not self.intersects0bs(i.point, j.point, obsVec):
                    distanceMap.append((self.getEuclideanDistance(i.point, j.point), j))
            distanceMap = sorted(distanceMap, key=lambda x: x[0])
            for count, pair in enumerate(distanceMap):
                if count >= 10:
                    break
                i.neighbors.append(pair[1])
    
    def solveShortestPath(self):
        dist = [float('inf')] * (self.numNodes + 2)
        dist[0] = 0
        prev = [-1] * (self.numNodes + 2)
        vset = [True] * (self.numNodes + 2)
        while any(vset):
            u = min((d, i) for i, d in enumerate(dist) if vset[i])[1]
            vset[u] = False
            for v in self.getById(u).neighbors:
                alt = dist[u] + self.getEuclideanDistance(self.getById(u).point, v.point)
                if alt < dist[v.node_id]:
                    dist[v.node_id] = alt
                    prev[v.node_id] = u
        path = []
        node = 1
        while node != -1:
            path.append(node)
            node = prev[node]
        return path

    def getEuclideanDistance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def isWithinWorld(self, p):
        return self.x_min <= p.x <= self.x_max and self.y_min <= p.y <= self.y_max
    
    def intersects0bs(self, p1, p2, obsVec):
        return False  # Simplified for now
    
    def getById(self, node_id):
        return next((node for node in self.nodes if node.node_id == node_id), None)
    
    def getNodes(self):
        return self.nodes

def plot_prm(nodes, path):
    plt.figure(figsize=(8, 8))
    # Plot edges (roadmap)
    for node in nodes:
        for neighbor in node.neighbors:
            plt.plot([node.point.x, neighbor.point.x], [node.point.y, neighbor.point.y], 'r-', alpha=0.5)
    # Plot nodes
    for node in nodes: 
        plt.plot(node.point.x, node.point.y, 'bo')
    # Plot shortest path
    for i in range(len(path) - 1):
        start = nodes[path[i]]
        end = nodes[path[i + 1]]
        plt.plot([start.point.x, end.point.x], [start.point.y, end.point.y], 'y', linewidth=2)
    # Highlight start and goal nodes
    plt.plot(nodes[0].point.x, nodes[0].point.y, 'go', markersize=10, label="Start")
    plt.plot(nodes[1].point.x, nodes[1].point.y, 'ro', markersize=10, label="Goal")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.title("Probabilistic Roadmap (PRM) with Shortest Path")
    plt.show() 

if __name__ == "__main__":
    rospy.init_node('prm_node', anonymous=True)
    # Load parameters from ROS Parameter Server
    x_max = rospy.get_param('~x_max', 20)
    x_min = rospy.get_param('~x_min', 0)
    y_max = rospy.get_param('~y_max', 20)
    y_min = rospy.get_param('~y_min', 0)
    numNodes = rospy.get_param('~numNodes', 50)
    # Initialize PRM and generate roadmap
    prm = PRM(x_max, x_min, y_max, y_min, numNodes)
    obsVec = []  # Adjust if you have obstacles data
    prm.generateRandomPoints(obsVec)
    prm.computeNeighborGraph(obsVec)
    # Solve shortest path
    path = prm.solveShortestPath()
    rospy.loginfo("Shortest path found: %s", path)
    # Visualize PRM and path
    plot_prm(prm.getNodes(), path)
