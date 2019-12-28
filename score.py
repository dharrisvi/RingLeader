"""
Ring Leader
"""

class Score(object):
    def __init__(self, nlp):
        self.score = 0
        self.next_level_points = nlp
        self.alerts = Alerts_List()

    def __iadd__(self, rhs):
        if type(rhs) is not list:
            rhs = [rhs]
        
        for alert in rhs:
            if type(alert) is tuple:
                alert = Alert(alert[0][0], alert[0][1], alert[1])
            
            p_max = self.next_level_points - self.score
            
            if alert.pts > p_max:
                alert.pts = p_max
            elif -alert.pts > self.score:
                alert.pts = -self.score

            self.score += alert.pts
            
            if alert.pts:
                self.alerts += alert
        
        return self

    def draw(self, screen, HEIGHT, WIDTH):
        # Draws the score and next level threshold in bottom left 
        screen.draw.text(f'{self.score}/{self.next_level_points}',
                         bottomleft=(10, HEIGHT-10))
        self.alerts.draw(screen, WIDTH)

    def is_new_level(self):
        if self.score >= self.next_level_points:
            return True
        
        return False
        
    def update(self, delta, HEIGHT):
        self.alerts.update(delta, HEIGHT)

class Alert(object):
    SCORE_VELOCITY = -.02 # Constant upward movement of score alerts
    SCORE_DURATION = 40 # Update cycles to display score alerts
    
    def __init__(self, x, y, pts):
        self.x = x
        self.y = y
        self.pts = pts
        self.life = Alert.SCORE_DURATION
        self.vely = Alert.SCORE_VELOCITY
    
    def __str__(self):
        atts = ['\t' + a + ': ' + str(v) for a,v in self.__dict__.items()]
        return type(self).__name__ + ' object:\n' + '\n'.join(atts)

    def draw(self, screen, WIDTH):
        x, y, m = self.x, self.y, self.pts
        if x > WIDTH: #Off screen to right, adjust
            screen.draw.text(f'{m:+d}', midright=(WIDTH, y))
        elif x < 0: #Off screen to left, adjust
            screen.draw.text(f'{m:+d}', midleft=(0, y))
        else:
            screen.draw.text(f'{m:+d}', midtop=(x, y))
            
class Alerts_List(object):
    def __init__(self):
        self.contents = []
    
    def __str__(self):
        if self.contents:
            s = 'Alerts_List:\n'
            s += '     x pos     y pos   pts   life    vely\n'
            for a in self.contents:
                s += f'{a.x:10.2f}{a.y:10.2f}{a.pts:6}{a.life:5}{a.vely:10.2f}\n'
        else:
            s = 'Empty Alerts_List:\n'
        return s

    def __len__(self):
        return len(self.contents)

    def __iter__(self):
        return iter(self.contents)

    def __getitem__(self, key):
        return self.contents[key]

    def __setitem__(self, key, item):
        self.contents[key] = item

    def __delitem__(self, key):
        del self.contents[key]
        
    def __iadd__(self, rhs):
        self.contents.append(rhs)
        return self

    def draw(self, screen, WIDTH):
        for a in self.contents: 
            a.draw(screen, WIDTH)
            
    def update(self, delta, HEIGHT):
        cnt = 0
        while cnt < len(self.contents):
            y, vely, life = (self.contents[cnt].y, 
                             self.contents[cnt].vely, 
                             self.contents[cnt].life)
            self.contents[cnt].life -= 1 # Decrement time to live
            if y > HEIGHT: # Move low alerts up on to screen
                self.contents[cnt].y = HEIGHT-5
            elif y < 5: # Move high alerts down 
                self.contents[cnt].y = 5
                self.contents[cnt].vely *= -1 # And make them float down instead of up
            self.contents[cnt].y += vely*delta[0] # Float up slowly
            if life < 0: # Time expired
                del self.contents[cnt]
            else:
                cnt += 1