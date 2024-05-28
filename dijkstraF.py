from collections import defaultdict

INF = float('infinity')


class DHeap:
    def __init__(self, d):
        self.heap = []
        self.d = d

    def length(self):
        return len(self.heap)

    def get_parent_index(self, child_index):
        return (child_index - 2) // self.d + 1

    def get_children(self, parent_index):
        children = []
        size = self.length()
        for i in range(self.d):
            child_index = (parent_index * self.d) + (i + 1)
            if child_index < size:
                children.append(self.heap[child_index])
            else:
                break
        return children

    def swap(self, index1, index2):
        tmp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = tmp

    def heapify(self, index, size):
        children = self.get_children(index)
        if len(children) == 0:
            return

        min_child_index = children.index(min(children))
        min_child_index = (self.d * index) + (min_child_index + 1)
        if self.heap[min_child_index][0] < self.heap[index][0]:
            self.swap(index, min_child_index)
            if min_child_index < size // self.d:
                self.heapify(min_child_index, size)

    def swim_up(self, index):
        if index == 0:
            return
        parent = self.get_parent_index(index)
        if self.heap[parent][0] < self.heap[index][0]:
            return
        self.swap(parent, index)
        self.swim_up(parent)

    def extract_min(self):
        self.swap(0, self.length()-1)
        result = self.heap.pop()
        self.heapify(0, self.length()-1)
        return result

    def insert(self, key):

        self.heap.append(key)
        self.swim_up(self.length() - 1)

    def __len__(self):
        return len(self.heap)


dist = []
parent = []
found = []
adj = defaultdict(list)


def dijkstra(s, n, m):

    heap = DHeap(m//n)

    for i in range(n):
        dist.append(INF)
        parent.append(-1)
        found.append(False)

    dist[s] = 0
    heap.insert((0, s))

    while len(heap) > 0:

        current_distance, current_vertex = heap.extract_min()
        if current_distance > dist[current_vertex]:
            continue

        for neighbor, weight in adj[current_vertex]:
            distance = current_distance + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heap.insert((distance, neighbor))


if __name__ == "__main__":

    n, m, s = map(int, input("").strip().split(" "))

    for i in range(m):
        x, y, w = map(int, input("").strip().split(" "))
        adj[x].append([y, w])

    dijkstra(s, n, m)

    for i in range(n):
        if dist[i] == INF:
            print(f"{i}\t{-1}")
        else:
            print(f"{i}\t{dist[i]}")
