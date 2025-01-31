import pygame, random, sys
from collections import deque
import heapq
from dataclasses import dataclass, field

DIST = 10

pygame.init()

width = 1280
height = 800

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

cols = width // 16
rows = height // 16
w = width // cols
h = height // rows

# accounts for duplicate keys to treat them items as insertion order
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: any = field(compare=False)

class Node:
    weight_range = 3
    gap = 1
    alpha_increment = 200 / weight_range
    overlays = []

    default_node_color = (100, 100, 100)
    start_color = (255, 0, 0)
    blocked_color = (0, 0, 0)
    visited_color = (40, 150, 80)
    path_color = (150, 40, 20)
    end_color = (0, 20, 255)
    for i in range(weight_range):
        overlay = pygame.Surface((w - gap, h - gap), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha_increment * i)
        overlays.append(overlay)

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.neighbors: list[Node] = []
        self.prev = None
        
        self.weight = random.randint(1, Node.weight_range)
        self.dist = 0
        
        self.blocked = False
        self.visited = False

        self.rect = pygame.Rect(self.x * w, self.y * h, w - Node.gap, h - Node.gap)

    def reset_path(self):
        self.dist = float('inf')
        self.prev = None
        self.blocked = False
        self.visited = False

    def draw(self, surface):
        color = Node.default_node_color
        if self.blocked:
            color = Node.blocked_color
        elif self.visited:
            color = Node.visited_color
        if self.prev is None and self.dist == 0:
            color = Node.start_color
        # if self.in_queue:
        #     pygame.draw.circle(surface, color, (self.x * w + w // 2, self.y * h + h // 2), w // 3) 
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(Node.overlays[self.weight - 1], (self.x * w, self.y * h))

    # if node in path:
    #     node.draw(screen, path_color)
    # if node in queue:
    #     node.draw(screen, (39, 175, 95), False)
    # if node == end:
    #     node.draw(screen, end_color)

# A directed weighted graph where the nodes carry the incoming weight value
# no need for adj matrix as a result
class Grid:
    def __init__(self, size):
        self.size = self.cols, self.rows = size
        self.size = size
        self.nodes: list[Node] = []
        self.load()
        print(len(self.nodes) * len(self.nodes[0]))

    def load(self):
        self.load_nodes()
        self.store_neighbor_refs()

    def load_nodes(self):
        for i in range(self.cols):
            temp_row = []
            for j in range(self.rows):
                temp_row.append(Node(i, j))
            self.nodes.append(temp_row)

    def store_neighbor_refs(self):
        for i in range(cols):
            for j in range(rows):
                self.add_neighbors_to_node(self.nodes[i][j])
    
    def add_neighbors_to_node(self, node: Node):
        # order added: left, right, top, bottom
        if node.x > 0:
            node.neighbors.append(self.nodes[node.x - 1][node.y])
        if node.x < self.cols - 1:
            node.neighbors.append(self.nodes[node.x + 1][node.y])
        if node.y < rows - 1:
            node.neighbors.append(self.nodes[node.x][node.y + 1])
        if node.y > 0:
            node.neighbors.append(self.nodes[node.x][node.y - 1])

    def reset_node_paths(self):
        for rows in self.nodes:
            for node in rows:
                node.reset_path()

    def calculate_movable(self, start_pos, movement_points):
        self.reset_node_paths()
        queue = []
        start = self.nodes[start_pos[0]][start_pos[1]]
        start.dist = 0
        heapq.heappush(queue, PrioritizedItem(0, start))

        while len(queue) > 0:
            current = heapq.heappop(queue).item
            for neighbor in current.neighbors:
                new_dist = current.dist + neighbor.weight
                if new_dist < neighbor.dist and new_dist <= movement_points:
                    neighbor.dist = new_dist
                    neighbor.prev = current
                    heapq.heappush(queue, PrioritizedItem(neighbor.dist, neighbor))
            current.visited = True

    def get_path(self, start_pos, end_pos):
        path = []
        end = self.nodes[end_pos[0], end_pos[1]]
        start = self.nodes[start_pos[0], start_pos[1]]
        current = end
        path.append((current.x, current.y))
        while current is not start:
            current = current.prev
            path.append((current.x, current.y))
            if current is None:
                return "No path between these nodes"
        return '->'.join(path)

    def draw(self, surface):
        for rows in self.nodes:
            for node in rows:
                node.draw(surface)

# def clickWall(pos, state):
#     x = pos[0] // w
#     y = pos[1] // h
#     grid[x][y].blocked = state

bg_color = (20, 20, 20)

no_path = False
path_found = False

running = True

grid = Grid((cols, rows))


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONUP:
            pass
        if e.type == pygame.MOUSEMOTION:
            pass
        if e.type == pygame.MOUSEBUTTONDOWN:
            pt = pygame.mouse.get_pos()
            for r in grid.nodes:
                for n in r:
                    if n.rect.collidepoint(pt):
                        grid.calculate_movable((n.x, n.y), DIST)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                grid.reset_node_paths()

    screen.fill(bg_color)
    grid.draw(screen)
    pygame.display.update()
