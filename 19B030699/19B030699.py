import json
import random
import uuid
from enum import Enum
from threading import Thread
import pygame
import pika

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
youwin = pygame.image.load('image\\youwin.jpg')
gameover = pygame.image.load('image\\gameover.png')
#backs = pygame.image.load('image\\backsingle.jpg')
tank = pygame.image.load('image\\tank.png')

screen = pygame.display.set_mode((800, 600))
#SinglePbg = pygame.image.load('SGback.jpg')

spritesheet = pygame.image.load("image\\spritetank.png")
spritesheet.convert()
sz = 220
w, h = 220, 90
tanksprite = []

tanksprite.append(spritesheet.subsurface((80, 87, 65, 80)))
tanksprite.append(spritesheet.subsurface((245, 87, 80, 65)))
tanksprite.append(spritesheet.subsurface((80, 205, 65, 80)))
tanksprite.append(spritesheet.subsurface((245, 210, 80, 65)))

upEnemy = tanksprite[0]
rightEnemy = tanksprite[1]
downEnemy = tanksprite[2]
leftEnemy = tanksprite[3]

upOwn = pygame.image.load('image\\up.png')
rightOwn = pygame.image.load('image\\right.png')
downOwn = pygame.image.load('image\\down.png')
leftOwn = pygame.image.load('image\\left.png')

shoot = pygame.mixer.Sound('sounds\\shoot.wav')
bump = pygame.mixer.Sound('sounds\\bump.wav')

bg = pygame.image.load("image\\mainmenu.jpg")

f1 = pygame.font.SysFont('serif', 50)
option1 = f1.render("Press m to play in single mode", True, (255, 0, 0))
bg.blit(option1, (100, 200))

f2 = pygame.font.SysFont('serif', 50)
option2 = f2.render("Press n to play in multiplayer mode", True, (255, 0, 0))
bg.blit(option2, (850, 200))

f3 = pygame.font.SysFont('serif', 50)
option3 = f3.render("Press f to play with bot ", True, (255, 0, 0))
bg.blit(option3, (550, 400))


menuloop = True
while menuloop:
    pygame.init()
    screen.blit(pygame.transform.scale(bg, (800, 600)), (0, 0))  # Until this place Main menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menuloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menuloop = False                                   #mainmenu functionality
            if event.key == pygame.K_m:                            #single player
                pygame.display.set_caption("Tanks")
                wall = pygame.image.load('image\\wall.jpg')
                start_time2 = None
                clock = pygame.time.Clock()

                class Direction(Enum):
                    UP = 1
                    DOWN = 2
                    LEFT = 3
                    RIGHT = 4



                def life_tank(n, x, y, s):
                    f = pygame.font.SysFont('serif', 30)
                    lifet2 = f.render(s + str(n), True, (12, 97, 23))
                    screen.blit(lifet2, (x, y))


                class Tank:

                    def __init__(self, x, y, speed, color, right, left, up, down, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT,d_up=pygame.K_UP, d_down=pygame.K_DOWN):
                        self.x = x
                        self.y = y
                        self.health = 3
                        self.speed = speed
                        self.color = color
                        self.width = 40
                        self.direction = Direction.RIGHT
                        self.right = right
                        self.left = left
                        self.up = up
                        self.down = down

                        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                                    d_up: Direction.UP, d_down: Direction.DOWN}

                    def draw(self):
                        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
                        pygame.draw.rect(screen, self.color,
                                         (self.x, self.y, self.width, self.width), 2)
                        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

                        if self.direction == Direction.RIGHT:
                            screen.blit(pygame.transform.scale(self.right, (self.width, self.width)), (self.x, self.y))

                        if self.direction == Direction.LEFT:
                            screen.blit(pygame.transform.scale(self.left, (self.width, self.width)), (self.x, self.y))

                        if self.direction == Direction.UP:
                            screen.blit(pygame.transform.scale(self.up, (self.width, self.width)), (self.x, self.y))

                        if self.direction == Direction.DOWN:
                            screen.blit(pygame.transform.scale(self.down, (self.width, self.width)), (self.x, self.y))

                    def change_direction(self, direction):
                        self.direction = direction

                    def move(self):
                        if self.direction == Direction.LEFT:
                            self.x -= self.speed
                        if self.direction == Direction.RIGHT:
                            self.x += self.speed
                        if self.direction == Direction.UP:
                            self.y -= self.speed
                        if self.direction == Direction.DOWN:
                            self.y += self.speed

                        if self.x > 800:
                            self.x = 0
                        if self.x < 0:
                            self.x = 800
                        if self.y > 600:
                            self.y = 0
                        if self.y < 0:
                            self.y = 600

                        self.draw()

                    def fire(self):
                        shoot.play()
                        if self.direction == Direction.LEFT:
                            bullet = Bullet(self.x - 20, self.y + 20, -10, 0, self.color)
                        if self.direction == Direction.RIGHT:
                            bullet = Bullet(self.x + 60, self.y + 20, 10, 0, self.color)
                        if self.direction == Direction.UP:
                            bullet = Bullet(self.x + 20, self.y - 20, 0, -10, self.color)
                        if self.direction == Direction.DOWN:
                            bullet = Bullet(self.x + 20, self.y + 60, 0, 10, self.color)
                        bullets.append(bullet)


                class Bullet:
                    def __init__(self, x, y, velx, vely, color):
                        self.x = x
                        self.y = y
                        self.brad = 4
                        self.velx = velx
                        self.vely = vely
                        self.color = color


                    def draw(self):
                        pygame.draw.circle(screen, self.color, (self.x, self.y), self.brad)

                    def move(self):
                        self.x += self.velx
                        self.y += self.vely

                        self.draw()

                class RandomWall:
                    def __init__(self, x, y):
                        self.x = x
                        self.y = y
                        self.width = 40
                        self.height = 40

                    def draw(self):
                        screen.blit(pygame.transform.scale(wall, (self.width, self.height)), (self.x, self.y))

                class SuperPower:
                    def __init__(self, x, y):
                        self.x = x
                        self.y = y
                        self.width = 25
                        self.height = 25

                    def draw(self):
                        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width , self.height))

                mainloop = True

                superpower = SuperPower(random.randint(100, 700), random.randint(100, 500))

                wall11 = RandomWall(random.randint(100, 700), random.randint(100, 500))
                wall12 = RandomWall(wall11.x + 30, wall11.y)
                wall13 = RandomWall(wall12.x + 30, wall12.y)

                wall21 = RandomWall(random.randint(100, 700), random.randint(100, 500))
                wall22 = RandomWall(wall21.x + 30, wall21.y)
                wall23 = RandomWall(wall22.x + 30, wall22.y)

                tank1 = Tank(300, 300, 2, (44, 50, 163), rightOwn, leftOwn, upOwn,downOwn)
                tank2 = Tank(100, 100, 2, (161, 40, 48), rightEnemy, leftEnemy, upEnemy, downEnemy, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)


                bullets = []

                FPS = 60
                clock = pygame.time.Clock()


                while mainloop:
                    mill = clock.tick(FPS)
                    #screen.blit(pygame.transform.scale(backs, (800, 600)), (0, 0))
                    start_time = pygame.time.get_ticks()
                    screen.fill((255, 255, 255))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            mainloop = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                mainloop = False

                            if event.key in tank1.KEY.keys():
                                tank1.change_direction(tank1.KEY[event.key])
                            if event.key in tank2.KEY.keys():
                                tank2.change_direction(tank2.KEY[event.key])

                            if event.key == pygame.K_SPACE:
                                tank1.fire()

                            if event.key == pygame.K_RETURN:
                                tank2.fire()

                    life_tank(tank1.health, 15, 15, 'Player 1: ')
                    life_tank(tank2.health, 15, 50, 'Player 2: ')

                    wall11.draw()
                    wall12.draw()
                    wall13.draw()
                    wall21.draw()
                    wall22.draw()
                    wall23.draw()

                    #tank1

                    if tank1.x in range(wall11.x, wall11.x + wall11.width) and tank1.y in range(wall11.y, wall11.y + wall11.height):
                        wall11 = RandomWall(2000, 3000)
                        tank1.health -= 1
                        bump.play()

                    if tank1.x in range(wall12.x, wall12.x + wall12.width) and tank1.y in range(wall12.y, wall12.y + wall12.height):
                        wall12 = RandomWall(2000, 3000)
                        tank1.health -= 1
                        bump.play()

                    if tank1.x in range(wall13.x, wall13.x + wall13.width) and tank1.y in range(wall13.y, wall13.y + wall13.height):
                        wall13 = RandomWall(2000, 3000)
                        tank1.health -= 1
                        bump.play()

                    if tank1.x in range(wall21.x, wall21.x + wall21.width) and tank1.y in range(wall21.y, wall21.y + wall21.height):
                        wall21 = RandomWall(2000, 3000)
                        tank1.health -= 1
                        bump.play()

                    if tank1.x in range(wall22.x, wall22.x + wall22.width) and tank1.y in range(wall22.y, wall22.y + wall22.height):
                        wall22 = RandomWall(2000, 3000)
                        tank1.health -= 1
                        bump.play()

                    if tank1.x in range(wall23.x, wall23.x + wall23.width) and tank1.y in range(wall23.y, wall23.y + wall23.height):
                        wall23 = RandomWall(2000, 3000)
                        tank1.health -= 1
                        bump.play()

                    #tank2

                    if tank2.x in range(wall11.x, wall11.x + wall11.width) and tank1.y in range(wall11.y, wall11.y + wall11.height):
                        wall11 = RandomWall(2000, 3000)
                        tank2.health -= 1
                        bump.play()

                    if tank1.x in range(wall12.x, wall12.x + wall12.width) and tank1.y in range(wall12.y,
                                                                                                wall12.y + wall12.height):
                        wall12 = RandomWall(2000, 3000)
                        tank2.health -= 1
                        bump.play()

                    if tank2.x in range(wall13.x, wall13.x + wall13.width) and tank1.y in range(wall13.y,
                                                                                                wall13.y + wall13.height):
                        wall13 = RandomWall(2000, 3000)
                        tank2.health -= 1
                        bump.play()

                    if tank2.x in range(wall21.x, wall21.x + wall21.width) and tank1.y in range(wall21.y,
                                                                                                wall21.y + wall21.height):
                        wall21 = RandomWall(2000, 3000)
                        tank2.health -= 1
                        bump.play()

                    if tank2.x in range(wall22.x, wall22.x + wall22.width) and tank1.y in range(wall22.y,
                                                                                                wall22.y + wall22.height):
                        wall22 = RandomWall(2000, 3000)
                        tank2.health -= 1
                        bump.play()

                    if tank2.x in range(wall23.x, wall23.x + wall23.width) and tank1.y in range(wall23.y,
                                                                                                wall23.y + wall23.height):
                        wall23 = RandomWall(2000, 3000)
                        tank2.health -= 1
                        bump.play()


                    for b in bullets:
                        b.move()

                        if b.x in range(tank1.x, tank1.x + 40) and b.y in range(tank1.y, tank1.y + 40):
                            bullets.pop(0)
                            tank1.health -= 1
                            bump.play()

                        if b.x in range(tank2.x, tank2.x + 40) and b.y in range(tank2.y, tank2.y + 40):
                            bullets.pop(0)
                            tank2.health -= 1
                            bump.play()



                        if b.x in range(wall11.x, wall11.x + wall11.width) and b.y in range(wall11.y, wall11.y + wall11.height):
                            wall11 = RandomWall(2000, 3000)
                            bump.play()
                            bullets.pop(0)

                        if b.x in range(wall12.x, wall12.x + wall12.width) and b.y in range(wall12.y, wall12.y + wall12.height):
                            wall12 = RandomWall(2000, 3000)
                            bump.play()
                            bullets.pop(0)

                        if b.x in range(wall13.x, wall13.x + wall13.width) and b.y in range(wall13.y, wall13.y + wall13.height):
                            wall13 = RandomWall(2000, 3000)
                            bump.play()
                            bullets.pop(0)

                        if b.x in range(wall21.x, wall21.x + wall21.width) and b.y in range(wall21.y, wall21.y + wall21.height):
                            wall21 = RandomWall(2000, 3000)
                            bump.play()
                            bullets.pop(0)

                        if b.x in range(wall22.x, wall22.x + wall22.width) and b.y in range(wall22.y, wall22.y + wall22.height):
                            wall22 = RandomWall(2000, 3000)
                            bump.play()
                            bullets.pop(0)

                        if b.x in range(wall23.x, wall23.x + wall23.width) and b.y in range(wall23.y, wall23.y + wall23.height):
                            wall23 = RandomWall(2000, 3000)
                            bump.play()
                            bullets.pop(0)

                    if tank1.health == 0 or tank2.health == 0:
                        mainloop = False

                    tank1.move()
                    tank2.move()

                    pygame.display.flip()

                pygame.quit()

            if event.key == pygame.K_n:                                                    #Multiplayer

                class TankRpcClient:

                    def __init__(self):
                        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=IP,
                            port=PORT,
                            virtual_host=VIRTUAL_HOST,
                            credentials=pika.PlainCredentials(
                                username=USERNAME,
                                password=PASSWORD
                            )
                        )
                        )  # подключение к серверу(connection)

                        self.channel = self.connection.channel()
                        queue = self.channel.queue_declare(queue='',
                                                           auto_delete=True,
                                                           exclusive=True
                                                           )

                        self.callback_queue = queue.method.queue
                        self.channel.queue_bind(
                            exchange='X:routing.topic',
                            queue=self.callback_queue
                        )  #binding

                        self.channel.basic_consume(
                            queue=self.callback_queue,
                            on_message_callback=self.on_response,
                            auto_ack=True
                        )

                        self.response = None
                        self.corr_id = None
                        self.token = None
                        self.tank_id = None
                        self.room_id = None
                        self.response = None

                    def on_response(self, ch, method, props, body):
                        if self.corr_id == props.correlation_id:
                            self.response = json.loads(body)
                            print(self.response)

                    def call(self, key, message={}):

                        self.response = None
                        self.corr_id = str(uuid.uuid4())
                        self.channel.basic_publish(
                            exchange='X:routing.topic',
                            routing_key=key,
                            properties=pika.BasicProperties(
                                reply_to=self.callback_queue,
                                correlation_id=self.corr_id,
                            ),
                            body=json.dumps(message)
                        )
                        while self.response is None:
                            self.connection.process_data_events()

                    def check_server_status(self):
                        self.call('tank.request.healthcheck')
                        return self.response['status'] == '200'

                    def obtain_token(self, room_id):
                        message = {
                            'roomId': room_id
                        }
                        self.call('tank.request.register', message)
                        if 'token' in self.response:
                            self.token = self.response['token']
                            self.tank_id = self.response['tankId']
                            self.room_id = self.response['roomId']
                            return True
                        return False


                    def turn_tank(self, token, direction):
                        message = {
                            'token': token,
                            'direction': direction
                        }
                        self.call('tank.request.turn', message)

                    def fire_bullet(self, token):
                        message = {
                            'token': token,
                        }
                        self.call('tank.request.fire', message)



                class TankConsumerClient(Thread):

                    def __init__(self, room_id):
                        super().__init__()
                        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=IP,
                            port=PORT,
                            virtual_host=VIRTUAL_HOST,
                            credentials=pika.PlainCredentials(
                                username=USERNAME,
                                password=PASSWORD
                            )
                        )
                        )  # подключение к серверу(connection)

                        self.channel = self.connection.channel()
                        queue = self.channel.queue_declare(queue='',
                                                           auto_delete=True,
                                                           exclusive=True
                                                           )

                        event_listener = queue.method.queue
                        self.channel.queue_bind(exchange='X:routing.topic',
                                                queue=event_listener,
                                                routing_key='event.state.'+room_id)
                        self.channel.basic_consume(
                            queue=event_listener,
                            on_message_callback=self.on_response,
                            auto_ack=True
                        )
                        self.response = None

                    def on_response(self, ch, method, props, body):
                        self.response = json.loads(body)
                        print(self.response)

                    def run(self):
                        self.channel.start_consuming()

                UP = 'UP'
                DOWN = 'DOWN'
                LEFT = 'LEFT'
                RIGHT = 'RIGHT'

                MOVE_KEYS = {
                    pygame.K_w: UP,
                    pygame.K_s: DOWN,
                    pygame.K_a: LEFT,
                    pygame.K_d: RIGHT
                }


                def draw_opponents_tank(x, y, width, height, direction):
                    if direction == 'UP':
                        screen.blit(pygame.transform.scale(upEnemy, (width, height)), (x, y))
                    if direction == 'DOWN':
                        screen.blit(pygame.transform.scale(downEnemy, (width, height)), (x, y))
                    if direction == 'RIGHT':
                        screen.blit(pygame.transform.scale(rightEnemy, (width, height)), (x, y))
                    if direction == 'LEFT':
                        screen.blit(pygame.transform.scale(leftEnemy, (width, height)), (x, y))

                def draw_own_tank(x, y, width, height, direction):
                    if direction == 'UP':
                        screen.blit(pygame.transform.scale(upOwn, (width, height)), (x, y))
                    if direction == 'DOWN':
                        screen.blit(pygame.transform.scale(downOwn, (width, height)), (x, y))
                    if direction == 'RIGHT':
                        screen.blit(pygame.transform.scale(rightOwn, (width, height)), (x, y))
                    if direction == 'LEFT':
                        screen.blit(pygame.transform.scale(leftOwn, (width, height)), (x, y))


                def draw_bullet(x, y):
                    pygame.draw.circle(screen, (255, 0, 255), (x, y), 4)

                def draw_own_bullets(x, y):
                    pygame.draw.circle(screen, (173, 255, 47), (x, y), 4)


                def life_own_tank(n, x, y):
                    f = pygame.font.SysFont('serif', 20)
                    lifet = f.render('Health of your tank: ' + str(n), True, (0, 0, 0))
                    screen.blit(lifet, (x, y))

                def score_own_tank(n, x, y):
                    f2 = pygame.font.SysFont('serif', 20)
                    lifet2 = f2.render('Score of your tank: ' + str(n), True, (0, 0, 0))
                    screen.blit(lifet2, (x, y))

                def scores_players(n, x, y):
                    f3 = pygame.font.SysFont('serif', 20)
                    lifet3 = f3.render('Score of tank: ' + str(n), True, (52, 255, 26))
                    screen.blit(lifet3, (x, y))

                #def score



                def game_start_multiplayer():
                    mainloop = True
                    while mainloop:
                        #screen.blit(pygame.transform.scale(backs, (800, 600)), (0, 0))
                        screen.fill((255, 255, 255))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                mainloop = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    mainloop = False
                                if event.key in MOVE_KEYS:
                                    client.turn_tank(client.token, MOVE_KEYS[event.key])
                                if event.key == pygame.K_SPACE:
                                    client.fire_bullet(client.token)
                                    shoot.play()

                        bullets = event_client.response['gameField']['bullets']
                        for bullet in bullets:
                            if client.tank_id == bullet['owner']:
                                bullet_x = bullet['x']
                                bullet_y = bullet['y']
                                draw_own_bullets(bullet_x, bullet_y)
                            else:
                                bullet_x = bullet['x']
                                bullet_y = bullet['y']
                                draw_bullet(bullet_x, bullet_y)

                        hits = event_client.response['hits']
                        for hit in hits:
                            if hit:
                                bump.play()


                        tanks = event_client.response['gameField']['tanks']
                        for tank in tanks:
                            if client.tank_id == tank['id']:
                                tank_x = tank['x']
                                tank_y = tank['y']
                                tank_width = tank['width']
                                tank_height = tank['height']
                                tank_direction = tank['direction']
                                draw_own_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)
                            else:
                                tank_x = tank['x']
                                tank_y = tank['y']
                                tank_width = tank['width']
                                tank_height = tank['height']
                                tank_direction = tank['direction']
                                draw_opponents_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)


                            tank_health = tank['health']
                            life_own_tank(tank_health, 15, 50)
                            tank_score = tank['score']
                            score_own_tank(tank_score, 300, 50)

                        winlose = event_client.response['winners']
                        for win in winlose:
                            if win == client.tank_id:
                                screen.blit(pygame.transform.scale(youwin, (800, 600)), (0, 0))
                            else:
                                screen.blit(pygame.transform.scale(gameover, (800, 600)), (0, 0))

                        pygame.display.flip()

                client = TankRpcClient()
                client.check_server_status()
                client.obtain_token('room-4')


                event_client = TankConsumerClient('room-4')
                event_client.start()
                game_start_multiplayer()


            if event.key == pygame.K_f:         #Artificial intelligenc
                class TankRpcClient:

                    def __init__(self):
                        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=IP,
                            port=PORT,
                            virtual_host=VIRTUAL_HOST,
                            credentials=pika.PlainCredentials(
                                username=USERNAME,
                                password=PASSWORD
                            )
                        )
                        )  # подключение к серверу(connection)

                        self.channel = self.connection.channel()
                        queue = self.channel.queue_declare(queue='',
                                                           auto_delete=True,
                                                           exclusive=True
                                                           )

                        self.callback_queue = queue.method.queue
                        self.channel.queue_bind(
                            exchange='X:routing.topic',
                            queue=self.callback_queue
                        )  # binding

                        self.channel.basic_consume(
                            queue=self.callback_queue,
                            on_message_callback=self.on_response,
                            auto_ack=True
                        )

                        self.response = None
                        self.corr_id = None
                        self.token = None
                        self.tank_id = None
                        self.room_id = None
                        self.response = None

                    def on_response(self, ch, method, props, body):
                        if self.corr_id == props.correlation_id:
                            self.response = json.loads(body)
                            print(self.response)

                    def call(self, key, message={}):

                        self.response = None
                        self.corr_id = str(uuid.uuid4())
                        self.channel.basic_publish(
                            exchange='X:routing.topic',
                            routing_key=key,
                            properties=pika.BasicProperties(
                                reply_to=self.callback_queue,
                                correlation_id=self.corr_id,
                            ),
                            body=json.dumps(message)
                        )
                        while self.response is None:
                            self.connection.process_data_events()

                    def check_server_status(self):
                        self.call('tank.request.healthcheck')
                        return self.response['status'] == '200'

                    def obtain_token(self, room_id):
                        message = {
                            'roomId': room_id
                        }
                        self.call('tank.request.register', message)
                        if 'token' in self.response:
                            self.token = self.response['token']
                            self.tank_id = self.response['tankId']
                            self.room_id = self.response['roomId']
                            return True
                        return False

                    def turn_tank(self, token, direction):
                        message = {
                            'token': token,
                            'direction': direction
                        }
                        self.call('tank.request.turn', message)

                    def fire_bullet(self, token):
                        message = {
                            'token': token,
                        }
                        self.call('tank.request.fire', message)


                class TankConsumerClient(Thread):

                    def __init__(self, room_id):
                        super().__init__()
                        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                            host=IP,
                            port=PORT,
                            virtual_host=VIRTUAL_HOST,
                            credentials=pika.PlainCredentials(
                                username=USERNAME,
                                password=PASSWORD
                            )
                        )
                        )  # подключение к серверу(connection)

                        self.channel = self.connection.channel()
                        queue = self.channel.queue_declare(queue='',
                                                           auto_delete=True,
                                                           exclusive=True
                                                           )

                        event_listener = queue.method.queue
                        self.channel.queue_bind(exchange='X:routing.topic',
                                                queue=event_listener,
                                                routing_key='event.state.' + room_id)
                        self.channel.basic_consume(
                            queue=event_listener,
                            on_message_callback=self.on_response,
                            auto_ack=True
                        )
                        self.response = None

                    def on_response(self, ch, method, props, body):
                        self.response = json.loads(body)
                        print(self.response)

                    def run(self):
                        self.channel.start_consuming()


                UP = 'UP'
                DOWN = 'DOWN'
                LEFT = 'LEFT'
                RIGHT = 'RIGHT'

                MOVE_KEYS = {
                    pygame.K_w: UP,
                    pygame.K_s: DOWN,
                    pygame.K_a: LEFT,
                    pygame.K_d: RIGHT
                }


                def draw_opponents_tank(x, y, width, height, direction):
                    if direction == 'UP':
                        screen.blit(pygame.transform.scale(upEnemy, (width, height)), (x, y))
                    if direction == 'DOWN':
                        screen.blit(pygame.transform.scale(downEnemy, (width, height)), (x, y))
                    if direction == 'RIGHT':
                        screen.blit(pygame.transform.scale(rightEnemy, (width, height)), (x, y))
                    if direction == 'LEFT':
                        screen.blit(pygame.transform.scale(leftEnemy, (width, height)), (x, y))


                def draw_own_tank(x, y, width, height, direction):
                    if direction == 'UP':
                        screen.blit(pygame.transform.scale(upOwn, (width, height)), (x, y))
                    if direction == 'DOWN':
                        screen.blit(pygame.transform.scale(downOwn, (width, height)), (x, y))
                    if direction == 'RIGHT':
                        screen.blit(pygame.transform.scale(rightOwn, (width, height)), (x, y))
                    if direction == 'LEFT':
                        screen.blit(pygame.transform.scale(leftOwn, (width, height)), (x, y))


                def draw_bullet(x, y):
                    pygame.draw.circle(screen, (255, 0, 255), (x, y), 4)


                def draw_own_bullets(x, y):
                    pygame.draw.circle(screen, (173, 255, 47), (x, y), 4)


                def life_own_tank(n, x, y):
                    f = pygame.font.SysFont('serif', 20)
                    lifet = f.render('Health of your tank: ' + str(n), True, (52, 255, 26))
                    screen.blit(lifet, (x, y))


                def score_own_tank(n, x, y):
                    f2 = pygame.font.SysFont('serif', 20)
                    lifet2 = f2.render('Score of your tank: ' + str(n), True, (52, 255, 26))
                    screen.blit(lifet2, (x, y))


                def scores_players(n, x, y):
                    f3 = pygame.font.SysFont('serif', 20)
                    lifet3 = f3.render('Score of tank: ' + str(n), True, (52, 255, 26))
                    screen.blit(lifet3, (x, y))


                # def score
                time = None
                def game_start_multiplayer():
                    mainloop = True
                    client.turn_tank(client.token, LEFT)
                    while mainloop:
                        screen.fill((255, 255, 255))
                        time = pygame.time.get_ticks()

                        if time:
                            time_since_enter = pygame.time.get_ticks() - time

                        if (time_since_enter % 20000) == 0:
                            client.fire_bullet(client.token)
                            if client.fire_bullet(client.token):
                                shoot.play()




                        client.turn_tank(client.token, LEFT)

                        res = None

                        bullets = event_client.response['gameField']['bullets']
                        for bullet in bullets:
                            if client.tank_id == bullet['owner']:
                                bullet_x = bullet['x']
                                bullet_y = bullet['y']
                                draw_own_bullets(bullet_x, bullet_y)
                            else:
                                bullet_x = bullet['x']
                                bullet_y = bullet['y']
                                draw_bullet(bullet_x, bullet_y)

                        hits = event_client.response['hits']
                        for hit in hits:
                            if hit:
                                bump.play()

                        tanks = event_client.response['gameField']['tanks']
                        for tank in tanks:
                            if client.tank_id == tank['id']:
                                tank_x = tank['x']
                                tank_y = tank['y']
                                tank_width = tank['width']
                                tank_height = tank['height']
                                tank_direction = tank['direction']
                                draw_own_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)

                                if tank_x > 700 and tank_y >100 and tank_y < 500:
                                    res = UP
                                if tank_x > 700 and tank_y < 100:
                                    res = DOWN
                                if tank_x > 700 and tank_y > 500:
                                    res = LEFT
                                if tank_x < 100 and tank_y > 500:
                                    res = RIGHT
                                if tank_x < 100 and tank_y < 100:
                                    res = RIGHT


                            else:
                                tank_x = tank['x']
                                tank_y = tank['y']
                                tank_width = tank['width']
                                tank_height = tank['height']
                                tank_direction = tank['direction']
                                draw_opponents_tank(tank_x, tank_y, tank_width, tank_height, tank_direction)

                            tank_health = tank['health']
                            life_own_tank(tank_health, 15, 50)
                            tank_score = tank['score']
                            score_own_tank(tank_score, 300, 50)


                        client.turn_tank(client.token, res)





                        winlose = event_client.response['winners']
                        for win in winlose:
                            if win == client.tank_id:
                                screen.blit(pygame.transform.scale(youwin, (800, 600)), (0, 0))
                            else:
                                screen.blit(pygame.transform.scale(gameover, (800, 600)), (0, 0))

                        pygame.display.flip()


                client = TankRpcClient()
                client.check_server_status()
                client.obtain_token('room-4')

                event_client = TankConsumerClient('room-4')
                event_client.start()
                game_start_multiplayer()

    pygame.display.flip()
pygame.display.flip
pygame.quit()