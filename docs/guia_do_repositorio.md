# Guia do projeto tracker.io

## Visão geral
- Projeto Django focado em rotina financeira e hábitos, com três apps: `accounts`, `finances`, `routines`.
- Baseia-se em configuração por ambiente via `.env` e em uma hierarquia de settings (base/dev/prod/test).
- Interfaces simples em HTML (Jinja/Django templates) e dependência total do stack padrão Django.

## Como o Django está configurado
- Ponto de entrada: `manage.py` define `DJANGO_SETTINGS_MODULE=config.settings` e delega à CLI do Django [manage.py](manage.py#L1-L22). Para entender comandos, veja a doc oficial de `manage.py`.
- Settings base carregam variáveis de ambiente com `python-dotenv`, definem apps, middleware, templates, banco e internacion./timezone [config/settings/base.py](config/settings/base.py#L1-L84).
  - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` vêm do `.env` em `BASE_DIR/.env`.
  - Banco padrão SQLite com possibilidade de Postgres via envs `DJANGO_DB_*` [config/settings/base.py](config/settings/base.py#L58-L68).
  - Internacionalização em pt-BR e fuso `America/Cuiaba` [config/settings/base.py](config/settings/base.py#L77-L80).
  - Arquivos estáticos servidos de `static/` durante dev [config/settings/base.py](config/settings/base.py#L82-L83).
- Perfis de ambiente:
  - Dev: apenas `DEBUG=True` herdando o resto [config/settings/dev.py](config/settings/dev.py#L1-L3).
  - Prod: força `DEBUG=False` e cookies/SSL mínimos [config/settings/prod.py](config/settings/prod.py#L1-L8).
  - Test: `DEBUG=False` e hash MD5 para testes rápidos [config/settings/test.py](config/settings/test.py#L1-L6).
- URL raiz inclui admin e delega para apps: finanças na raiz, contas em `/accounts/`, rotinas em `/routines/` [config/urls.py](config/urls.py#L17-L25).

## Apps e domínio
### common
- `TimeStampedModel` fornece `created_at/updated_at` para herança [common/models.py](common/models.py#L1-L8).
- `month_range` retorna início do mês e primeiro dia do próximo mês, base para agregações [common/utils.py](common/utils.py#L1-L10).

### accounts
- Models ainda vazios (espaço para perfil do usuário) [apps/accounts/models.py](apps/accounts/models.py#L1).
- URLs plugam `LoginView` e `LogoutView` do Django Auth, usando template custom [apps/accounts/urls.py](apps/accounts/urls.py#L1-L9).
- Template de login minimalista estende layout base [apps/accounts/templates/accounts/login.html](apps/accounts/templates/accounts/login.html#L1-L9).

### finances
- Modelos de domínio financeiro [apps/finances/models.py](apps/finances/models.py#L5-L50):
  - `Account`: conta financeira do usuário; única por `owner+name` [apps/finances/models.py](apps/finances/models.py#L5-L17).
  - `Category`: categoria de gasto/receita única por usuário+nome [apps/finances/models.py](apps/finances/models.py#L18-L28).
  - `Transaction`: movimentação com tipo `IN/OUT`, valor decimal, data (`occurred_at`), descrição e índices por data/tipo [apps/finances/models.py](apps/finances/models.py#L30-L50).
- Admin expõe os modelos com filtros e busca (erro tipográfico em `ownner` pode quebrar a busca) [apps/finances/admin.py](apps/finances/admin.py#L1-L20).
- Serviço transacional `create_transaction` valida a posse de conta/categoria antes de criar a transação [apps/finances/services.py](apps/finances/services.py#L6-L51).
- Selector `monthly_summary` agrega receitas, despesas, saldo e ranking por categoria usando `month_range` [apps/finances/selectors.py](apps/finances/selectors.py#L7-L38).
- View protegida por login monta o dashboard com o resumo do mês atual [apps/finances/views.py](apps/finances/views.py#L7-L15) e é roteada na raiz do site [apps/finances/urls.py](apps/finances/urls.py#L1-L8).
- Template do dashboard mostra valores e lista categorias ou mensagem vazia [apps/finances/templates/finances/dashboard.html](apps/finances/templates/finances/dashboard.html#L1-L21).

### routines
- Estrutura para hábitos: `Habit` (nome único por usuário) e `HabitCheckin` (check-in diário único) [apps/routines/models.py](apps/routines/models.py#L5-L31).
- URLs ainda vazias aguardando endpoints [apps/routines/urls.py](apps/routines/urls.py#L1-L7).

### templates base
- Layout global simples com `<main>` centralizado e bloco `{% block content %}` [templates/base.html](templates/base.html#L1-L13).

## Fluxo principal hoje
1. Usuário acessa `/` → `dashboard` exige autenticação; se não logado, redireciona para login.
2. Login usa `LoginView` com template custom; após autenticar, retorna à página desejada.
3. `dashboard` chama `monthly_summary` (mês atual) → agrega transações do usuário.
4. Template renderiza receitas, despesas, saldo e despesas por categoria.

## Conceitos para estudar
- Django básico: projeto vs apps, settings, URLs, views, templates, ORM, admin. Referência: https://docs.djangoproject.com/en/stable/intro/
- Autenticação e autorização: `LoginView`, `LogoutView`, `@login_required`, `AUTH_USER_MODEL`. https://docs.djangoproject.com/en/stable/topics/auth/default/
- Modelos e consultas: `ForeignKey`, `TextChoices`, `UniqueConstraint`, índices, agregações `Sum`. https://docs.djangoproject.com/en/stable/topics/db/models/ e https://docs.djangoproject.com/en/stable/topics/db/aggregation/
- Transações: `transaction.atomic` para garantir consistência ao criar registros relacionados. https://docs.djangoproject.com/en/stable/topics/db/transactions/
- Templates: blocos, herança, contextos. https://docs.djangoproject.com/en/stable/topics/templates/
- Configuração por ambientes e dotenv: boas práticas para segredos/flags (`DEBUG`, `ALLOWED_HOSTS`). Leia também o Deployment Checklist do Django: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

## Decisões e porquês
- Separação de settings (base/dev/prod/test) facilita alternar configurações sem duplicar lógica [config/settings/__init__.py](config/settings/__init__.py#L1-L6).
- Uso de `TimeStampedModel` evita repetir campos de auditoria e mantém consistência [common/models.py](common/models.py#L3-L8).
- Constraints de unicidade por usuário nos modelos impedem duplicatas de nomes dentro do mesmo dono, refletindo regras de negócio.
- Índices em `Transaction` otimizam filtros por data/tipo usados no dashboard [apps/finances/models.py](apps/finances/models.py#L43-L47).
- `transaction.atomic` protege a criação de transações com validação de ownership para evitar registros órfãos [apps/finances/services.py](apps/finances/services.py#L6-L51).
- Selector isolado (`monthly_summary`) separa lógica de consulta da view, facilitando testes e reuso [apps/finances/selectors.py](apps/finances/selectors.py#L7-L38).

## Pontos de atenção / próximos passos
- Completar o app `accounts` com modelo de perfil caso necessário; hoje é só autenticação padrão.
- Implementar URLs/views para hábitos (`routines`) e templates correspondentes.
- Adicionar testes para services/selectors e para garantir as constraints.
- Criar paginação/UX melhor para dashboard e internacionalização dos valores (formatação monetária).
