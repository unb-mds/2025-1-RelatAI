# Anotações sobre Criação de APIs com Django REST Framework

## Introdução ao Django REST Framework (DRF)

- **O que é**: Uma biblioteca poderosa que facilita a construção de APIs RESTful em Django.

- **Por que usar**: Oferece ferramentas para serialização, autenticação, permissões e visualizações, simplificando o desenvolvimento de APIs robustas.

## Componentes Principais do DRF

### 1. Serializers

- **Função**: Convertem complexos objetos de dados (como querysets) em tipos de dados nativos do Python, que podem ser facilmente renderizados em JSON ou XML.

- **Uso**: Facilitam a validação e transformação de dados de entrada e saída.

### 2. Views e ViewSets

- **Views**: Controlam a lógica para lidar com requisições HTTP e retornam respostas apropriadas.

- **ViewSets**: Agrupam lógica relacionada, permitindo operações CRUD de forma mais eficiente e organizada.

### 3. Routers

- **Função**: Automatizam o roteamento de URLs para os ViewSets, reduzindo a necessidade de configuração manual de cada rota.

### 4. Autenticação e Permissões

- **Autenticação**: DRF suporta diversos esquemas, como tokens e OAuth.

- **Permissões**: Controlam o acesso aos endpoints da API, garantindo que apenas usuários autorizados possam interagir com determinados recursos.

## Passos para Criar uma API com DRF

1. **Instalação**:

   ```bash
   pip install djangorestframework
   ```


2. **Configuração**:

   - Adicionar `'rest_framework'` ao `INSTALLED_APPS` no `settings.py`.

3. **Definir Modelos**:

   - Criar modelos no `models.py` que representam os dados da aplicação.

4. **Criar Serializers**:

   - No `serializers.py`, definir classes que convertem os modelos para JSON e vice-versa.

5. **Implementar ViewSets**:

   - No `views.py`, criar classes que herdam de `ViewSet` ou `ModelViewSet` para definir o comportamento das views.

6. **Configurar Rotas**:

   - Utilizar `routers` para mapear automaticamente URLs para os ViewSets.

## Exemplo Prático

**Definindo o Modelo**:


```python
from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    curso = models.CharField(max_length=100)
```


**Criando o Serializer**:


```python
from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'
```


**Implementando o ViewSet**:


```python
from rest_framework import viewsets
from .models import Aluno
from .serializers import AlunoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
```


**Configurando as Rotas**:


```python
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
```


## Recursos Adicionais

- [Tutorial Oficial do Django REST Framework](https://www.django-rest-framework.org/tutorial/quickstart/)

- [Vídeo: Django Markdown Tutorial - A Simple Blog Example](https://www.youtube.com/watch?v=t61nTi0lIlk)

Essas anotações fornecem uma visão geral dos conceitos e passos fundamentais para criar APIs utilizando o Django REST Framework. 