import pygame, random, sys
from collections import deque
import heapq
from dataclasses import dataclass, field

DIST = 25

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
        self.dist = float('inf')
        
        self.blocked = False
        self.visited = False
        self.path = False

        self.rect = pygame.Rect(self.x * w, self.y * h, w - Node.gap, h - Node.gap)

    def reset_pathfind(self):
        self.dist = float('inf')
        self.prev = None
        self.visited = False
        self.path = False

    def draw(self, surface, color_override=None):
        color = Node.default_node_color
        if self.path:
            color = Node.path_color
        elif self.blocked:
            color = Node.blocked_color
        elif self.visited:
            color = Node.visited_color
        if self.prev is None and self.dist == 0:
            color = Node.start_color
        if color_override:
            color = color_override
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
        # print(len(self.nodes) * len(self.nodes[0]))

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

    def reset_pathfind(self):
        for rows in self.nodes:
            for node in rows:
                node.reset_pathfind()
    
    def reset_path(self):
        for rows in self.nodes:
            for node in rows:
                node.path = False

    def calculate_movable(self, start_pos, movement_points):
        self.reset_pathfind()
        queue = []
        start = self.nodes[start_pos[0]][start_pos[1]]
        start.dist = 0
        heapq.heappush(queue, PrioritizedItem(0, start))

        while len(queue) > 0:
            current = heapq.heappop(queue).item
            for neighbor in current.neighbors:
                new_dist = current.dist + neighbor.weight
                if new_dist < neighbor.dist and new_dist <= movement_points and not neighbor.blocked:
                    neighbor.dist = new_dist
                    neighbor.prev = current
                    heapq.heappush(queue, PrioritizedItem(neighbor.dist, neighbor))
            current.visited = True

    def get_path(self, start_pos, end_pos):
        self.reset_path()
        path = []
        curr_end = self.nodes[end_pos[0]][end_pos[1]]
        curr_start = self.nodes[start_pos[0]][start_pos[1]]
        current = curr_end
        while current is not curr_start:
            if current is None:
                print("No Path")
                return "No path between these nodes"
            current.path = True
            path.append(f'{current.x}, {current.y}')
            current = current.prev
        print(path)
        return '->'.join(path)

    def draw(self, surface):
        for rows in self.nodes:
            for node in rows:
                node.draw(surface)
                if node == end:
                    node.draw(surface, Node.end_color)
                

bg_color = (20, 20, 20)
running = True
grid = Grid((cols, rows))
path_calculated = False
start = None
end = None

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
            print(pt)
            for r in grid.nodes:
                for n in r:
                    if n.rect.collidepoint(pt):
                        if e.button == 1:
                            start = (n.x, n.y)
                            print(f'calculating path of {n.x},{n.y}')
                            grid.calculate_movable(start, DIST)
                            path_calculated = True
                        elif e.button == 2 and path_calculated:
                            end = n
                            end_coords = (n.x, n.y)
                            grid.get_path(start, end_coords)
                        elif e.button == 3:
                            print(f'{n.x},{n.y} blocked')
                            n.blocked = not n.blocked
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                grid.reset_pathfind()
                path_calculated = False
                start = None
                end = None

    screen.fill(bg_color)
    grid.draw(screen)
    pygame.display.update()
