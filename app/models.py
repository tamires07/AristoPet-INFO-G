from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    data_nasc = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    email = models.EmailField(unique=True, verbose_name="Email")
    senha = models.CharField(max_length=128, verbose_name="Senha")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    imagem = models.ImageField(upload_to='animais/', blank=True, null=True, verbose_name="Foto de Perfil")

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)
    
    def __str__(self):
        return f"{self.nome}, {self.data_nasc}, {self.endereco}, {self.email}, {self.senha}, {self.telefone}, {self.imagem}"

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"


class Instituicao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Instituição")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    email = models.EmailField(verbose_name="Email")
    senha = models.CharField(max_length=100, verbose_name="Senha")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")

    def __str__(self):
        return f"{self.nome}, {self.cnpj}, {self.endereco}, {self.email}, {self.senha}, {self.telefone}"

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"

class Animal(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Animal")
    especie = models.CharField(max_length=50, verbose_name="Espécie")
    genero = models.CharField(max_length=50, verbose_name="Gênero")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    doador = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Doador")
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='animais/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome}, {self.especie}, {self.genero}, {self.cidade}, Doador: {self.doador}, {self.imagem}"

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animais"

class Adocao(models.Model):
    doador = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Doador")
    adotante = models.ForeignKey(Pessoa, related_name='adotante', on_delete=models.CASCADE, verbose_name="Adotante")
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    data_adocao = models.DateField(auto_now_add=True, verbose_name="Data de Adoção")

    def __str__(self):
        return f"{self.doador}, {self.adotante},{self.animal}, {self.data_adocao}"

    class Meta:
        verbose_name = "Adoção"
        verbose_name_plural = "Adoções"

class Evento(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Evento")
    instituicao = models.CharField(max_length=200, verbose_name="Instituição")
    data_hora = models.DateTimeField(verbose_name="Data e Hora do Evento")
    local = models.CharField(max_length=200, verbose_name="Local do Evento")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    site_instituicao = models.URLField(max_length=500, blank=True, null=True, verbose_name="Link do site") 

    def __str__(self):
        return f"{self.nome}, {self.instituicao}, {self.data_hora}, {self.local}, {self.cidade}, {self.site_instituicao}"

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

class Conversa(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    participante_doador = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="conversas_como_doador")
    participante_adotante = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="conversas_como_adotante")
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Conversa"
        verbose_name_plural = "Conversas"

class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name="mensagens")
    remetente = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['data_envio']

    def __str__(self):
        return f"{self.remetente.nome}: {self.texto[:20]}..."