# tracker.io
Projeto em Django para estudo..

### Descrição completa em [docs/guia_do_repositorio.md](docs/guia_do_repositorio.md).

### Notas pessoais em [docs/notes.md](docs/notes.md).

### Pensamento lógico do projeto
- Projeto criado para estudo e prática de Django, focado em gerenciamento financeiro e hábitos.
- Estrutura modular com três apps principais: `accounts` (autenticação), `finances` (gestão financeira) e `routines` (hábitos).
- Configuração por ambiente usando arquivos `.env` e hierarquia de settings para facilitar desenvolvimento e produção.
- Uso de modelos Django para representar contas, categorias, transações e hábitos, com validações e relacionamentos adequados.
- Implementação de views protegidas por autenticação, serviços para lógica de negócio e seletores para agregações de dados.
- Interface simples baseada em templates Django, focada na funcionalidade essencial.
### Estrutura típica de um app Django neste projeto
| Arquivo | Função |
|---------|--------|
| models.py | Definição dos modelos de dados |
| forms.py | Validar dados de entrada do user e UX |
| tests.py | Garantir qualidade e prevenir bugs |
| services.py | Lógica de negócio complexa |
| selectors.py | Consultas complexas e agregações |