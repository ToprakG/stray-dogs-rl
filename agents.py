import mesa
import random
import math

class Dog(mesa.Agent):
    def __init__(self, model, age, sex, rabid, sterilized, vaccinated, adoptability, bred, health_status, location, reproductive_status, aggression_level, day_count=0):
        super().__init__(model)
        self.model = model
        self.age = age  # Age in months
        self.sex = sex
        self.rabid = rabid
        self.sterilized = sterilized
        self.vaccinated = vaccinated
        self.adoptability = adoptability
        self.bred = bred
        self.health_status = health_status
        self.location = location
        self.pos = location  # Position in the grid
        self.reproductive_status = reproductive_status
        self.aggression_level = aggression_level
        self.pack = []  # Pack members
        self.hunger = 0
        self.is_in_pack = False  # Whether the dog is part of a pack
        self.territory_center = None  # The center of the dog's territory
        self.last_move_together = 0  # Time since the dog last moved with its pack
        self.season = "Spring"
        self.day_count = day_count

    def step(self):
        """Advance the model by one step (which represents a month)."""
        self.age += 1  # Increment age by 1 day

        self.day_count += 1 # Increment the day count

        # Change the season every 100 days (approx. every season)
        if self.day_count % 100 == 0:
            self.change_season()

        # Increase the hunger
        self.hunger += 10

        if self.hunger >= 200:
            print("The dog has died.")
            self.remove()

        # Set reproductive status based on age
        if self.age >= 730:  # 2 years = 24 months
            self.reproductive_status = "active"

        self.check_lifespan()  # Check if the dog dies
        self.reproduce()  # Check for reproduction
        self.move()  # Move
        self.interact_with_nearby_agents()  # Interact with others

        # Apply neutering and vaccination rates weekly
        if random.random() < self.model.neutering_rate:
            self.sterilize()
        if random.random() < self.model.vaccination_rate:
            self.vaccinate()

        # Pack behavior: Check if the dog is close to other dogs and might form a pack
        self.check_pack_behavior()

    def move(self):
        """Randomly move to an adjacent position, or move with the pack."""
        if self.is_in_pack and random.random() < 0.7:  # 70% chance to move with the pack if in a pack
            self.move_with_pack()
        else:
            self.random_move()

    def random_move(self):

        if self.age > 1800:
            inactivity_luck = random.randint(0,1)
            if inactivity_luck == 1:
                """Move randomly to an adjacent position."""
                empty_neighbors = self.model.grid.get_neighborhood(
                    self.pos, moore=True, include_center=False, radius=1
                )

                moves = [
                    (1, 0),   # Move right
                    (-1, 0),  # Move left
                    (0, -1),  # Move up
                    (0, 1),   # Move down
                ]

                dx, dy = random.choice(moves)

                new_position = (
                    (self.pos[0] + dx) % self.model.grid.width,
                    (self.pos[1] + dy) % self.model.grid.height,
                )

                if new_position in empty_neighbors:
                    self.model.grid.move_agent(self, new_position)
            else:
                pass
        else:
            """Move randomly to an adjacent position."""
            empty_neighbors = self.model.grid.get_neighborhood(
                    self.pos, moore=True, include_center=False, radius=1
                )

            moves = [
                    (1, 0),   # Move right
                    (-1, 0),  # Move left
                    (0, -1),  # Move up
                    (0, 1),   # Move down
            ]

            dx, dy = random.choice(moves)

            new_position = (
                    (self.pos[0] + dx) % self.model.grid.width,
                    (self.pos[1] + dy) % self.model.grid.height,
            )

            if new_position in empty_neighbors:
                self.model.grid.move_agent(self, new_position)

    def move_with_pack(self):
        """Move to the center of the pack's territory."""
        if self.territory_center:
            dx = self.territory_center[0] - self.pos[0]
            dy = self.territory_center[1] - self.pos[1]

            # Move towards the center of the pack's territory
            if abs(dx) > 1:
                dx = 1 if dx > 0 else -1
            if abs(dy) > 1:
                dy = 1 if dy > 0 else -1

            new_position = (
                round((self.pos[0] + dx) % self.model.grid.width),
                round((self.pos[1] + dy) % self.model.grid.height),
            )

            self.model.grid.move_agent(self, new_position)
            print(f"Dog at {self.pos} moved with the pack to {new_position}")

    def sterilize(self):
        """Sterilize the dog."""
        if not self.sterilized:
            self.sterilized = True
            print(f"Dog at {self.pos} has been sterilized.")

    def vaccinate(self):
        """Vaccinate the dog."""
        if not self.vaccinated:
            self.vaccinated = True
            print(f"Dog at {self.pos} has been vaccinated.")

    def reproduce(self):
        """Handle reproduction behavior."""
        if self.age >= 730 and not self.sterilized and self.reproductive_status == "active":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)

            for neighbor in neighbors:
                if isinstance(neighbor, Dog) and neighbor.sex != self.sex and neighbor.reproductive_status == "active":
                    if random.random() < 0.5:  # Random chance to reproduce (50%)
                        self.breed(neighbor)

    def breed(self, mate):
        """Create a new puppy when two dogs mate."""
        puppy_age = 0
        puppy_sex = random.choice(["M", "F"])
        puppy_rabid = random.choice([True, False])
        puppy_sterilized = False
        puppy_vaccinated = False
        puppy_adoptability = random.random()
        puppy_bred = False
        puppy_health_status = "healthy"
        puppy_location = self.pos
        puppy_reproductive_status = "inactive"
        puppy_aggression_level = random.random()

        puppy = Dog(self.model, puppy_age, puppy_sex, puppy_rabid, puppy_sterilized, puppy_vaccinated, puppy_adoptability,
                    puppy_bred, puppy_health_status, puppy_location, puppy_reproductive_status, puppy_aggression_level, self.day_count)

        self.model.grid.place_agent(puppy, puppy_location)
        print(f"A puppy was born at {puppy_location}!")

    def check_lifespan(self):
        if self.age <= 120:
            if random.random() < 0.4:
                self.remove()
        elif self.age <= 240:
            if random.random() < 0.8:
                self.remove()
        elif self.age > random.randint(3600, 5400):
            self.remove()

        # Age-related mortality risk
        elif self.age > 1800:  # Dogs older than 5 years
            if random.random() < 0.2:  # 20% chance of dying every year after 5 years
                self.remove()

        # Environmental factors (Winter and Hunger)
        elif self.season == "Winter" and self.hunger > 150:
            if random.random() < 0.5:  # 50% chance of dying due to hunger in winter
                self.remove()

        # Rabies or disease mortality
        elif self.rabid and random.random() < 0.3:  # 30% chance to die from rabies
            self.remove()

        # Injury mortality
        elif self.health_status == "injured":
            if random.random() < 0.2:  # 20% chance to die from injuries
                self.remove()


    def check_pack_behavior(self):
        """Check if the dog is close enough to form a pack."""
        if not self.is_in_pack:
            nearby_dogs = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=2)
            pack_candidates = [dog for dog in nearby_dogs if isinstance(dog, Dog) and not dog.is_in_pack]

            if len(pack_candidates) >= 2:  # Minimum of 3 dogs to form a pack
                self.form_pack(pack_candidates)

    def form_pack(self, pack_candidates):
        """Form a pack and set a territory."""
        pack_candidates.append(self)  # Include this dog in the pack
        self.is_in_pack = True

        # Set the pack's territory center (average position of pack members)
        pack_x = sum([dog.pos[0] for dog in pack_candidates]) / len(pack_candidates)
        pack_y = sum([dog.pos[1] for dog in pack_candidates]) / len(pack_candidates)
        self.territory_center = (pack_x, pack_y)

        # Set each dog in the pack to know they are in a pack
        for dog in pack_candidates:
            dog.is_in_pack = True
            dog.territory_center = self.territory_center

        print(f"A pack has been formed at {self.territory_center}!")

    def interact_with_nearby_agents(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)

        for neighbor in neighbors:
            if isinstance(neighbor, Human):
                if self.interact_with_human(neighbor):
                    print("Dog bit a human!")
            elif isinstance(neighbor, Dog):
                if self.interact_with_dog(neighbor):
                    print("Dog bit another dog!")

    def interact_with_human(self, human):
        distance = self.calculate_distance(human.location)
        if distance < 5:
            if self.rabid and random.random() < 0.05:
                human.get_rabies()
            if random.random() < 1 / 20 or self.pack and random.random() < 1/10 :  # 1 in every 73 humans is bitten
                return True
        return False

    def interact_with_dog(self, other_dog):
        if self.aggression_level > other_dog.aggression_level:
            if random.random() < 0.3:  # Increased chance of dogs biting each other
                other_dog.health_status = "injured"
                return True
        return False

    def calculate_distance(self, other_location):
        return math.sqrt((self.location[0] - other_location[0]) ** 2 + (self.location[1] - other_location[1]) ** 2)

    def adopt(self):
        self.remove()

    def feed(self):
        self.hunger -= 30
        self.aggression_level -= 20

    def change_season(self):
        seasons = ["Spring", "Summer", "Fall", "Winter"]
        current_season_index = seasons.index(self.season)
        self.season = seasons[(current_season_index + 1) % 4]

        print(f"Season changed to: {self.season}")

        self.apply_seasonal_changes()
    
    def apply_seasonal_changes(self):
        if self.season == "Winter":
            self.hunger += 15
            self.aggression_level -= 0.1

        elif self.season == "Summer":
            # Increase dog activity
            self.hunger -= 15
            self.aggression_level += 0.1
        
        elif self.season == "Fall":
            self.hunger += 7
            self.aggression_level -= 0.05

        elif self.season == "Spring":
            self.hunger -= 5
            self.aggression_level += 0.05



class Human(mesa.Agent):
    def __init__(self, model, age, sex, attitude_towards_dogs, location):
        super().__init__(model)
        self.age = age
        self.sex = sex
        self.attitude_towards_dogs = attitude_towards_dogs
        self.location = location
        self.pos = location
        self.rabid = False
        self.health_status = "healthy"
        self.rabies_duration = 0  # Tracks how long the human has been infected
        self.previous_money_spent = 0

    def step(self):
        self.age += 1
        self.check_rabies()
        self.move()  # Humans move every step
        self.interact_with_nearby_dogs()

        if self.model.attitude_spending > self.previous_money_spent:
            if random.randint(0,1) == 1:
                self.attitude_towards_dogs += 0.3
            else:
                pass

            self.previous_money_spent = self.model.attitude_spending
        else:
            self.previous_money_spent = self.model.attitude_spending

        
    def make_decision(self, dog):
        if dog.adoptability > 0.5 and self.attitude_towards_dogs > 0.7:
            dog.adopt()
            return "adopt"
        elif dog.health_status == "sick":
            dog.feed()
            return "feed"
        return "ignore"
    
    def get_rabies(self):
        """Handle the human getting rabies."""
        self.rabid = True
        self.rabies_duration = 1  # Start the rabies infection duration
        print(f"Human at {self.pos} has contracted rabies!")

    def check_rabies(self):
        """Check if the human dies from rabies or recovers."""
        if self.rabid:
            self.rabies_duration += 1  # Increase the duration of rabies infection

            # If the human has been infected for too long, they have a chance of dying
            if self.rabies_duration >= 5 and random.random() < 0.05:  # 5% chance of dying if infected for 5+ months
                self.health_status = "dead"
                print(f"Human at {self.pos} has died from rabies!")
                self.remove()

            # After some time, rabies could go away (human recovers)
            elif self.rabies_duration >= 5 and random.random() < 0.2:  # 20% chance of recovery after 5 months
                self.rabid = False
                print(f"Human at {self.pos} has recovered from rabies!")

    def move(self):
        """Randomly move to an adjacent position."""
        empty_neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False, radius=1
        )

        moves = [
            (1, 0),   # Move right
            (-1, 0),  # Move left
            (0, -1),  # Move up
            (0, 1),   # Move down
        ]

        dx, dy = random.choice(moves)

        new_position = (
            (self.pos[0] + dx) % self.model.grid.width,
            (self.pos[1] + dy) % self.model.grid.height,
        )

        if new_position in empty_neighbors:
            self.model.grid.move_agent(self, new_position)

    def interact_with_nearby_dogs(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)

        for neighbor in neighbors:
            if isinstance(neighbor, Dog):
                self.make_decision(neighbor)
    