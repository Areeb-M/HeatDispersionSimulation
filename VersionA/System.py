

class System:
    DISSIPATION_RATE = 50000

    def __init__(self, width, height, default_energy=0.0):
        self.width = width
        self.height = height
        self.grid = [[default_energy for h in range(height)] for w in range(width)]
        self.contact_cache = {}

    def add_heat(self, pos, amount):
        self.grid[pos[0]][pos[1]] += amount

    def remove_heat(self, pos, amount):
        self.grid[pos[0]][pos[1]] -= amount

    def exchange_heat(self, a, b, amount):
        self.grid[a[0]][a[1]] -= amount
        self.grid[b[0]][b[1]] += amount

    def apply_entropy(self, time):
        max_transfer = System.DISSIPATION_RATE * time
        queue = []

        for w in range(self.width):
            for h in range(self.height):
                contact_points = self.get_contact_points([w, h])
                differences = [[pos, (self.grid[w][h] - self.grid[pos[0]][pos[1]])/2.0] for pos in contact_points]
                differences = list(filter(lambda x: x[1] > 0, differences))
                if len(differences) == 0:
                    continue
                total = sum([d[1] for d in differences])
                weights = [d[1]/total for d in differences]
                change = max_transfer if total > max_transfer else total if total < self.grid[w][h] else self.grid[w][h]
                for i in range(len(differences)):
                    queue.append([[w, h], differences[i][0], change*weights[i]/2.0])

        for args in queue:
            self.exchange_heat(args[0], args[1], args[2])

    def get_contact_points(self, pos):
        hash_string = str(pos)
        if hash_string in self.contact_cache:
            return self.contact_cache[hash_string]
        else:
            self.contact_cache[hash_string] = self.get_contacts(pos)
            return self.contact_cache[hash_string]

    def get_contacts(self, pos):
        contact_points = [
            [pos[0]-1, pos[1]],
            [pos[0], pos[1]+1],
            [pos[0]+1, pos[1]],
            [pos[0], pos[1]-1]
        ]

        for i in range(3, -1, -1):
            if contact_points[i][0] < 0 or contact_points[i][0] >= self.width:
                del contact_points[i]
                continue
            if contact_points[i][1] < 0 or contact_points[i][1] >= self.height:
                del contact_points[i]

        return contact_points

    def generate_maximum_entropy(self):
        total = 0.0

        for row in self.grid:
            for space in row:
                total += space

        average = total / (self.width * self.height)
        self.grid = [[average for h in range(self.height)] for w in range(self.width)]