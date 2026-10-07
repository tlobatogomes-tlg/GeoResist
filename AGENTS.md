# AGENTS.md — GeoResist

## 1. Objetivo do projeto

GeoResist é um software profissional para apoio a projetos e serviços de engenharia geotécnica.

O sistema deve evoluir de forma modular, segura, testável e orientada às práticas de engenharia geotécnica brasileiras.

Áreas principais:
- Projetos
- Furos de sondagem
- SPT
- Estratigrafia
- Interpretação geotécnica
- Perfis estratigráficos
- Relatórios
- Banco de dados
- Futuramente frontend, mapas, GPS, fotografias e recursos offline

## 2. Estrutura atual

O backend está em:

backend/app/

Principais módulos:

- calculations/spt/
- calculations/estratigrafia/
- models/
- routers/
- schemas/
- tests/

Tecnologias atuais:
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- pytest
- Uvicorn

## 3. Regra fundamental: não quebrar o que já funciona

Antes de modificar código existente:

1. Entender a implementação atual.
2. Verificar os testes existentes.
3. Fazer alterações pequenas e isoladas.
4. Executar os testes relacionados.
5. Executar a suíte completa quando necessário.
6. Não remover funcionalidades existentes sem autorização explícita.

Não substituir uma implementação funcional por uma solução simplificada apenas para reduzir código.

## 4. SPT

O SPT deve manter separadas as informações de:

- golpes;
- penetrações;
- condições de execução;
- registro de campo;
- cálculo do N-SPT;
- interpretação.

O motor SPT já possui tratamento para condições como:

- normal;
- peso de haste;
- peso de martelo;
- sem avanço;
- não executado;
- cravação interrompida;
- cravação incompleta;
- penetração excepcional.

Não alterar essas regras sem analisar os testes existentes e sem justificar tecnicamente a mudança.

## 5. Estratigrafia

SPT e estratigrafia são informações diferentes.

SPT representa principalmente resistência à penetração e dados de execução.

Estratigrafia representa:
- profundidade inicial;
- profundidade final;
- origem;
- descrição do material;
- cor;
- complementos;
- observações.

As camadas não devem ser criadas automaticamente apenas porque existe um registro SPT.

## 6. Regra importante sobre ATERRO

ATERRO representa uma origem/classificação do material.

Uma mudança na descrição tátil-visual do material NÃO significa automaticamente o fim do aterro.

Exemplo:

0,00–0,45 m — aterro — argila silto-arenosa
0,45–1,45 m — aterro — argila arenosa

Nesse caso, o aterro continua de 0,00 até 1,45 m.

A base do aterro somente deve ser interpretada quando houver evidência de mudança de origem para material natural ou outra condição tecnicamente justificável.

Nunca interromper automaticamente um aterro a cada metro de SPT ou a cada mudança de descrição.

## 7. Continuidade do perfil

O perfil estratigráfico deve preservar a sequência real das camadas.

Camadas adjacentes são permitidas.

Sobreposições de intervalos devem ser rejeitadas.

Lacunas devem ser detectadas e sinalizadas.

Não preencher automaticamente uma lacuna com uma camada inventada.

## 8. Qualidade e validação

Toda nova regra importante deve possuir teste automatizado.

Ao alterar:
- motor SPT → executar testes SPT;
- motor de estratigrafia → executar testes de estratigrafia;
- API → testar endpoints afetados;
- modelos → verificar criação e funcionamento do banco.

Não considerar uma funcionalidade concluída apenas porque o código importa sem erro.

## 9. Testes atuais

Os testes existentes estão em:

backend/tests/

Eles são parte fundamental do projeto e devem ser preservados.

Antes de considerar uma alteração concluída, executar os testes relevantes.

## 10. Banco de dados

O projeto utiliza SQLite atualmente.

O arquivo de banco local não deve ser versionado pelo Git.

Não apagar ou recriar o banco de dados sem autorização explícita.

Alterações de modelos devem considerar compatibilidade com dados existentes.

## 11. API

A API utiliza FastAPI.

Rotas existentes incluem:
- projetos;
- furos;
- registros SPT;
- camadas/estratigrafia.

Ao criar novas rotas:
- seguir o padrão existente;
- usar schemas Pydantic;
- validar entradas;
- retornar erros HTTP apropriados;
- preservar consistência dos nomes em português utilizados pelo projeto.

## 12. Normas técnicas

O projeto deverá considerar as normas ABNT aplicáveis quando uma funcionalidade depender delas.

Não inventar requisitos normativos.

Quando houver dúvida sobre uma norma, sinalizar a necessidade de verificação da fonte normativa antes de implementar uma regra como obrigatória.

## 13. Idioma

Código pode utilizar nomes técnicos em português quando isso já fizer parte da arquitetura existente.

Mensagens da API destinadas ao usuário devem permanecer em português do Brasil, salvo decisão posterior do projeto.

## 14. Segurança das alterações

Não executar comandos destrutivos sem autorização explícita.

Não apagar:
- arquivos;
- banco de dados;
- testes;
- backups;
- histórico Git.

Não executar reset, clean, checkout destrutivo ou comandos equivalentes sem autorização.

## 15. Git

O repositório principal é:

https://github.com/tlobatogomes-tlg/GeoResist

Branch principal:

main

Antes de grandes alterações:
- verificar git status;
- preservar alterações existentes;
- criar commits pequenos e descritivos.

## 16. Princípio de desenvolvimento

Priorizar nesta ordem:

1. Correção técnica
2. Integridade dos dados
3. Testabilidade
4. Clareza do código
5. Conformidade com regras geotécnicas
6. Evolução da arquitetura
7. Interface e produtividade

O GeoResist deve evoluir como software de engenharia profissional, e não apenas como um CRUD.

## 17. Regra para o Codex

Antes de implementar uma solicitação:

1. Inspecionar os arquivos relacionados.
2. Entender o comportamento atual.
3. Identificar testes existentes.
4. Propor ou implementar a menor alteração coerente.
5. Testar.
6. Informar claramente quais arquivos foram alterados e quais testes foram executados.

Não assumir que uma regra geotécnica está correta apenas porque parece intuitiva.
