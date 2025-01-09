import numpy as np

class MoveCalculator:
    """This class contains all movement logic for prey objects"""
    def __init__(
            self, screen_width, screen_height,
            wall_thickness, cost_weights
            ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.wall_thickness = wall_thickness
        self.cost_weights = cost_weights

        # Create cost grids
        self.wall_cost_magnitude, self.wall_cost_x, self.wall_cost_y = self._create_wall_cost_grids()

        self.pos_cost_magnitude, self.pos_cost_x, self.pos_cost_y = self._create_position_cost_grids()
    
    def _create_wall_cost_grids(self):
        """Initialize the wall cost grid based on screen dimensions
        and wall thickness"""
        mag_grid = np.zeros((self.screen_height, self.screen_width))
        x_grid = np.zeros((self.screen_height, self.screen_width))
        y_grid = np.zeros((self.screen_height, self.screen_width))

        # top wall 
        mag_grid[:self.wall_thickness, :] = self.cost_weights["wall"]
        x_grid[:self.wall_thickness, :self.screen_width // 2] = 0 # Leftward
        x_grid[:self.wall_thickness, self.screen_width // 2:] = np.pi # Rightward
        y_grid[:self.wall_thickness, :] = 1.5 * np.pi # Downward

        # bottom wall vals
        mag_grid[-self.wall_thickness:, :] = self.cost_weights["wall"]
        x_grid[-self.wall_thickness:, :self.screen_width // 2] = 0 # Leftward
        x_grid[-self.wall_thickness:, self.screen_width //2:] = np.pi # Rightward
        y_grid[-self.wall_thickness, :] = 0.5 * np.pi # Upward

        # left wall vals
        mag_grid[:, :self.wall_thickness] = self.cost_weights["wall"]
        x_grid[:, :self.wall_thickness] = 0 # Rightward
        y_grid[:self.screen_height // 2, :self.wall_thickness] = 1.5 * np.pi # Upward
        y_grid[self.screen_height // 2:, :self.wall_thickness] = 0.5 * np.pi # Downward

        # right wall vals
        mag_grid[:, -self.wall_thickness:] = self.cost_weights["wall"]
        x_grid[:, -self.wall_thickness:] = np.pi # Leftward
        y_grid[:self.screen_height // 2, -self.wall_thickness:] = 1.5 * np.pi # Upward
        y_grid[self.screen_height // 2:, -self.wall_thickness:] = 0.5 * np.pi # Downward

        return mag_grid, x_grid, y_grid

    def _create_position_cost_grids(self):
        """Create a gradient cost grid that incentivizes staying near the center"""
        x, y = np.meshgrid(np.arange(self.screen_width), np.arange(self.screen_height))
        center_x, center_y = self.screen_width / 2, self.screen_height / 2

        # map grid
        mag_grid = np.sqrt(((x - center_x) / self.screen_width) ** 4 + ((y - center_y) / self.screen_height) ** 4)
        mag_grid = (mag_grid / np.max(mag_grid)) * self.cost_weights["position"]

        # direction grids
        radius_h = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        x_grid = np.pi - np.arccos((x - center_x) / radius_h)
        y_grid = np.pi - np.arcsin((y - center_y) / radius_h)

        return mag_grid, x_grid, y_grid

    def calculate_next_move(self, npc_pos, player_position, other_npcs, prev_positions):
        """Calculate the next move for an NPC based on various metrics"""
        npc_x, npc_y = int(npc_pos[0]), int(npc_pos[1])

        # Positional cost vector
        pos_vec = (
            self.pos_cost_magnitude[npc_y, npc_x]
            * np.array([
                np.cos(self.pos_cost_x[npc_y, npc_x]),
                -np.sin(self.pos_cost_y[npc_y, npc_x])
            ])
        )

        # Wall cost vector
        wall_vec = (
            self.wall_cost_magnitude[npc_y, npc_x]
            * np.array([
                np.cos(self.wall_cost_x[npc_y, npc_x]),
                -np.sin(self.wall_cost_y[npc_y, npc_x])
            ])
        )

        # player influence
        player_vec = self._calculate_player_influence(npc_pos, player_position)

        # NPC avoidance
        npc_avoidance_vec = self._calculate_npc_avoidance(npc_pos, other_npcs)

        # Momentum
        momentum_vec = self._calculate_momentum(prev_positions)

        # summed vector
        total_vec = pos_vec + wall_vec + player_vec + npc_avoidance_vec + momentum_vec
        total_vec = self._normalize_vector(total_vec)

        return total_vec
    
    def _calculate_player_influence(self, npc_pos, player_pos):
        vec_to_player = npc_pos - player_pos
        return self._normalize_vector(vec_to_player) * self.cost_weights["player_distance"]
        
    def _calculate_npc_avoidance(self, npc_pos, other_npcs):
        avoidance_vec = np.zeros(2)
        for other_pos in other_npcs:
            if not np.array_equal(npc_pos, other_pos):
                distance_vec = npc_pos - other_pos
                avoidance_vec += self._normalize_vector(distance_vec) * self.cost_weights["npc_distance"]
        return avoidance_vec

    def _calculate_momentum(self, prev_positions):
        if len(prev_positions) < 2:
            return np.zeros(2)
        momentum = prev_positions[-1] - prev_positions[-2]
        return self._normalize_vector(momentum) * self.cost_weights["momentum"]

    def _normalize_vector(self, vector):
        norm = np.linalg.norm(vector)
        return vector / norm if norm > 0 else np.zeros_like(vector)