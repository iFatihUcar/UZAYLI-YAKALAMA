import pygame
import random

pygame.init()

class DusenKareler():
    def __init__(self,DKareX,DKareY,KarelerResim,Hız):
        self.DKareX = DKareX
        self.DKareY = DKareY
        self.KarelerResim = KarelerResim
        self.Hız = Hız

    def Cizim(self,Pencere):
        Pencere.blit(self.KarelerResim,(self.DKareX,self.DKareY))

    def Hareket(self):
        self.DKareY += self.Hız

    def Kordinatlar(self,Genislik,Yukseklik):
        return pygame.Rect(self.DKareX, self.DKareY, Genislik, Yukseklik)

class BizimOyunumuz():
    def __init__(self):
        self.pencere_yuksekligi = 720
        self.pencere_genisligi = 1280
        self.Pencere = pygame.display.set_mode((self.pencere_genisligi,self.pencere_yuksekligi))
        pygame.display.set_caption("Kare Yakalama")
        self.Clock = pygame.time.Clock()

        self.ArkaPlan = pygame.image.load("Resimler/space.jpg").convert_alpha()
        self.BizimKare = pygame.image.load("Resimler/kare.jpg").convert_alpha()
        self.YakalaKare = pygame.image.load("Resimler/kare2.jpg").convert_alpha()

        self.Start = pygame.image.load("Resimler/Basla.jpg").convert_alpha()
        self.Exit =  pygame.image.load("Resimler/Cikis.jpg").convert_alpha()
        self.Retry = pygame.image.load("Resimler/retry.jpg").convert_alpha()

        self.BizimKaremiz = DusenKareler(600,620, self.BizimKare,0)

        self.OyunFont = pygame.font.SysFont("Lucida Console", 40, bold = True)
        self.GameOverFont = pygame.font.SysFont("Lucida Console", 100, bold = True)

        self.KareSayısı = 5
        self.KareListesi = []

        self.Skor = 0

        self.Durum = "Start"

        self.MinHız = 4
        self.MaxHız = 5
        
        self.Esik = 0
        
        self.Time = pygame.time.get_ticks()
        self.Sure = 9999999999999
        
    def Cizim(self):

        self.Pencere.blit(self.ArkaPlan,(0,0))

        if self.Durum == "Start":
            self.Pencere.blit(self.GameOverFont.render("UZAYLI YAKALAMA", True, (255, 0, 0)), (150, 300))
            self.Pencere.blit(self.Start,(550,500))

        elif self.Durum =="Oyun":
            self.Pencere.blit(self.OyunFont.render("SKOR = " + str(self.Skor), True, (255,255,255)), (20, 50))
            for DusKare in self.KareListesi:
                DusKare.Cizim(self.Pencere)
            self.BizimKaremiz.Cizim(self.Pencere)

        elif self.Durum == "GameOver":
            self.Pencere.blit(self.GameOverFont.render("GAME OVER", True, (255,0,0)), (350, 200))
            self.Pencere.blit(self.OyunFont.render("SKORUNUZ = " + str(self.Skor), True, (255,255,255)), (500, 350))
            self.Pencere.blit(self.Retry,(450,500))
            self.Pencere.blit(self.Exit,(730,500))

        self.Clock.tick(60)
        pygame.display.update()

    def Oyun(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Son"
        self.Tus = pygame.key.get_pressed()
        if self.Tus[pygame.K_ESCAPE]:
            return "Son"

        if self.Durum == "Start":
            self.mX, self.mY = pygame.mouse.get_pos()

            if ((550 < self.mX < 500+160) and ( 500 < self.mY < 500+90)) and pygame.mouse.get_pressed()[0] == 1:
                self.Time = pygame.time.get_ticks()
                self.Durum = "Oyun"

        elif self.Durum == "Oyun":
            self.Sure = 60000
            
            if pygame.time.get_ticks() - self.Time > self.Sure:
                self.Durum = "GameOver"
                                
            if self.Tus[pygame.K_a] and self.BizimKaremiz.DKareX > 0:
                self.BizimKaremiz.DKareX -= 20
            elif self.Tus[pygame.K_d] and self.BizimKaremiz.DKareX < 1180:
                self.BizimKaremiz.DKareX += 20


            if len(self.KareListesi) != self.KareSayısı:
                self.KareListesi.append(DusenKareler(random.randint(100,1200),-10,self.YakalaKare,random.randint(self.MinHız,self.MaxHız)))

            for DusKare in self.KareListesi:
                DusKare.Hareket()

                if DusKare.DKareY > 720:
                    DusKare.DKareY = -10
                    DusKare.DKareX = random.randint(100,1200)
                    self.Skor -= 1

                if (self.BizimKaremiz.Kordinatlar(100,100)).colliderect(DusKare.Kordinatlar(20,20)):
                    self.Skor += 1
                    DusKare.DKareY = -10
                    DusKare.DKareX = random.randint(100, 1200)
                    DusKare.Hız = random.randint(self.MinHız,self.MaxHız)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Ses/Yakalama.wav"))
                    
                if self.Skor % 10 == 0 and self.Skor > self.Esik:
                    self.MinHız += 1
                    self.MaxHız += 1
                    self.Esik += 10 

            if self.Skor < -5:
                self.Durum = "GameOver"

        elif self.Durum == "GameOver":
            self.mX, self.mY = pygame.mouse.get_pos()
            if ((450 < self.mX < 450 + 180) and (500 < self.mY < 500 + 120)) and pygame.mouse.get_pressed()[0] == 1:
                self.Skor = 0
                self.KareListesi.clear()
                self.BizimKaremiz.DKareX = 600
                self.Durum = "Oyun"
                self.Time = pygame.time.get_ticks()
            elif ((730 < self.mX < 730 + 180) and (500 < self.mY < 500 + 120)) and pygame.mouse.get_pressed()[0] == 1:
                return "Son"
                    
        self.Cizim()

Oyun = BizimOyunumuz()

while True:
    Durum = Oyun.Oyun()
    if Durum == "Son":
        break

pygame.quit()
