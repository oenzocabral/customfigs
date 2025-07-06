# Documentação do Projeto CustomFigs

## Visão Geral

O CustomFigs é uma plataforma Django que permite aos usuários criar e participar de eventos de figurinhas colecionáveis. Cada evento possui seu próprio conjunto de figurinhas (figures) com diferentes níveis de raridade, que os usuários podem adquirir através de pacotes aleatórios.

## Estrutura do Projeto

O projeto está organizado em 4 aplicativos principais:

1.  - Configurações principais do projeto
2. oenzocabral - Gerenciamento de usuários personalizados
3.  - Criação e gerenciamento de eventos
4.  - Sistema de figurinhas colecionáveis

## 1. Configurações Principais (customfigs_core)

### settings.py

- **AUTH_USER_MODEL**: Define o modelo de usuário personalizado ()
- **MEDIA_URL/MEDIA_ROOT**: Configurações para upload de imagens
- **LOGIN/LOGOUT URLs**: Redirecionamentos padrão para autenticação

### urls.py

Rotas principais que incluem:
- Painel admin
- URLs dos aplicativos oenzocabral,  e 
- Configuração para servir arquivos de mídia em desenvolvimento

## 2. Aplicativo Users

### Models

**CustomUser** (herda de AbstractUser):
- : Texto descritivo do usuário
- : Imagem de perfil
- Relacionamentos:
  - : Eventos criados pelo usuário (ForeignKey em Event)
  - : Álbuns pertencentes ao usuário (ForeignKey em Album)
  - : Figurinhas possuídas pelo usuário (ForeignKey em UserFigure)

### Forms

- **CustomUserCreationForm**: Formulário para registro de novos usuários
- **CustomUserChangeForm**: Formulário para edição de perfil

### Views

- **register**: Criação de nova conta
- **profile**: Visualização do próprio perfil
- **edit_profile**: Edição das informações do perfil
- **user_detail**: Visualização de perfis públicos de outros usuários

### URLs

-  - Registro de novo usuário
-  - Autenticação
-  - Perfil do usuário logado
-  - Perfil público de outros usuários

## 3. Aplicativo Events

### Models

**Event**:
- : Nome do evento
- : Descrição detalhada
- : Período de duração
- : Criador do evento (relacionamento com CustomUser)
- : Custo para participar
- : Status de ativação

Métodos:
- : Verifica se o evento está ocorrendo no momento

### Forms

**EventForm**:
- Valida datas (início deve ser anterior ao fim)
- Impede criação de eventos no passado

### Views

- **create_event**: Criação de novos eventos (apenas para usuários autenticados)
- **event_list**: Listagem de todos os eventos ativos
- **event_detail**: Detalhes de um evento específico
- **buy_ticket**: Aquisição de ingresso para um evento

### URLs

-  - Lista de eventos
-  - Criação de evento
-  - Detalhes do evento
-  - Compra de ingresso

## 4. Aplicativo Figures

### Models

**Figure**:
- : Nome da figurinha
- : Descrição
- : Imagem representativa
- : Raridade (common, uncommon, rare, etc.)
- : Evento ao qual pertence

**Album**:
- : Evento relacionado
- : Dono do álbum
- : Visibilidade pública

**UserFigure**:
- : Figurinha base
- : Dono atual
- : Álbum onde está armazenada
- : Status de venda
- : Preço (se estiver à venda)

**FigurePackage**:
- : Evento relacionado
- : Custo do pacote
- : Status de ativação

### Forms

- **FigureForm**: Criação de novas figurinhas
- **AlbumVisibilityForm**: Controle de visibilidade do álbum
- **FigureSaleForm**: Configuração de venda de figurinhas
- **FigureTransferForm**: Transferência entre usuários
- **FigurePackageForm**: Criação de pacotes de figurinhas

### Views

- **create_figure**: Adiciona novas figurinhas a um evento
- **album_detail**: Visualização de um álbum específico
- **buy_package**: Compra de pacote com 10 figurinhas aleatórias
- **set_figure_for_sale**: Coloca figurinha no mercado
- **transfer_figure**: Transfere figurinha para outro usuário
- **create_package**: Cria novo pacote de figurinhas
- **marketplace**: Lista de figurinhas à venda
- **buy_figure**: Compra de figurinha específica

### URLs

-  - Cria figurinha
-  - Detalhes do álbum
-  - Compra de pacote
-  - Vender figurinha
-  - Transferir figurinha
-  - Mercado de trocas

## Fluxos Principais

### 1. Criação de Evento

1. Usuário autenticado acessa 
2. Preenche formulário com detalhes do evento
3. Após criação, é redirecionado para página do evento

### 2. Participação em Evento

1. Usuário visualiza evento em 
2. Clica em Buy Ticket ()
3. Sistema cria um álbum vazio para o usuário naquele evento

### 3. Adição de Figurinhas (Criador)

1. Criador do evento acessa 
2. Preenche detalhes da figurinha (nome, imagem, raridade)
3. Figurinha fica disponível para inclusão em pacotes

### 4. Compra de Pacote

1. Usuário com ingresso acessa página do evento
2. Clica em Buy Package em um dos pacotes disponíveis
3. Sistema gera 10 figurinhas aleatórias e as adiciona ao álbum

### 5. Gerenciamento de Coleção

1. Usuário acessa seu álbum em 
2. Pode:
   - Alterar visibilidade (público/privado)
   - Vender figurinhas individuais
   - Transferir figurinhas para outros usuários

### 6. Mercado de Trocas

1. Todas as figurinhas marcadas para venda aparecem em 
2. Outros usuários podem comprar figurinhas disponíveis

## Considerações de Implementação

1. **Segurança**:
   - Todas as views de modificação usam 
   - Verificações de propriedade antes de edições
   - Forms com validação customizada

2. **Performance**:
   - Uso de  para otimizar queries
   - Agregações para estatísticas de raridade

3. **Extensibilidade**:
   - Modelos preparados para adição de novos campos
   - Sistema de permissões pode ser expandido

4. **Áreas para Melhoria**:
   - Implementação real de pagamentos
   - Algoritmo mais sofisticado para distribuição de raridades
   - Sistema de notificações para trocas

Esta documentação cobre os principais aspectos do sistema. Cada componente foi projetado para ser modular e de fácil manutenção, permitindo futuras expansões de funcionalidades.
