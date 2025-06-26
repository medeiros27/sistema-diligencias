# Manual do Usuário - Sistema de Diligências

## Visão Geral

O Sistema de Diligências é uma ferramenta completa para controle e gestão de diligências jurídicas, permitindo o cadastro, acompanhamento e relatórios de demandas e correspondentes.

## Funcionalidades Principais

### 1. Gestão de Diligências
- Cadastro de novas diligências
- Edição de diligências existentes
- Controle de status (Pendente, Cumprida, Cancelada)
- Acompanhamento de valores e pagamentos

### 2. Tipos de Demanda Suportados
- Audiência
- Cópia
- Protocolo
- Citação
- Intimação
- Outros

### 3. Relatórios e Exportação
- Estatísticas gerais do sistema
- Exportação para Excel
- Backup automático dos dados

## Como Usar

### Iniciando o Sistema
1. Execute o arquivo `SistemaDiligencias.exe` (Windows) ou o executável correspondente
2. A interface principal será exibida com as abas disponíveis

### Cadastrando Nova Diligência

1. **Menu Arquivo → Nova Diligência** ou clique no botão "Nova"
2. Preencha os campos obrigatórios:
   - **Data Solicitação**: Data em que a diligência foi solicitada
   - **Solicitante**: Nome da pessoa/empresa solicitante
   - **Tipo Demanda**: Selecione o tipo na lista
3. Campos opcionais:
   - **Telefone**: Contato do solicitante
   - **Nº Processo**: Número do processo judicial
   - **Data Demanda**: Quando a diligência deve ser realizada
   - **Horário**: Horário específico
   - **Local**: Local de realização
   - **Valor a Receber**: Valor cobrado pela diligência
   - **Observações**: Informações adicionais
4. Clique em "Salvar"

### Editando Diligência

1. Selecione a diligência na lista
2. Clique em "Editar" ou use **Menu Arquivo → Editar**
3. Modifique os campos necessários
4. Clique em "Salvar"

### Excluindo Diligência

1. Selecione a diligência na lista
2. Clique em "Excluir"
3. Confirme a exclusão

### Atualizando Status

Para marcar uma diligência como cumprida:
1. Edite a diligência
2. Altere o campo "Status" para "Cumprida"
3. Preencha a data de pagamento se aplicável
4. Salve as alterações

## Relatórios e Estatísticas

### Visualizando Estatísticas
1. **Menu Ferramentas → Estatísticas**
2. Visualize:
   - Total de diligências por status
   - Valores faturados e recebidos
   - Custos com correspondentes

### Exportando para Excel
1. **Menu Arquivo → Exportar Excel**
2. O arquivo será salvo na pasta de exportações
3. Contém todas as diligências com formatação adequada

## Backup e Segurança

### Backup Manual
1. **Menu Ferramentas → Backup**
2. Um backup será criado automaticamente na pasta de backups

### Backup Automático
- O sistema cria backups automáticos a cada 7 dias
- Mantém até 30 backups históricos
- Backups são salvos em `backups/`

## Estrutura de Dados

### Localização dos Dados
- **Windows**: `%APPDATA%/SistemaDiligencias/`
- **Linux/macOS**: `~/.sistema_diligencias/`

### Pastas Criadas
- `data/`: Banco de dados principal
- `logs/`: Arquivos de log do sistema
- `backups/`: Backups automáticos
- `exports/`: Arquivos exportados

## Formatos de Data

- **Entrada**: dd/mm/aaaa (ex: 15/03/2024)
- **Exibição**: dd/mm/aaaa
- **Armazenamento**: aaaa-mm-dd (formato ISO)

## Validações

### Telefone
- Aceita formatos: (11) 99999-9999, 11999999999
- Valida números com 10 ou 11 dígitos

### Email
- Validação básica de formato
- Deve conter @ e domínio válido

### Campos Obrigatórios
- Solicitante
- Tipo de Demanda
- Data de Solicitação

## Atalhos de Teclado

- **Ctrl+N**: Nova diligência
- **F5**: Atualizar lista
- **Delete**: Excluir selecionada
- **Ctrl+E**: Exportar Excel

## Solução de Problemas

### Erro ao Salvar
- Verifique se todos os campos obrigatórios estão preenchidos
- Confirme o formato das datas (dd/mm/aaaa)
- Verifique se há espaço em disco suficiente

### Dados não Aparecem
- Clique em "Atualizar" na aba de diligências
- Verifique os logs em caso de erro persistente

### Backup Falhou
- Verifique permissões de escrita na pasta
- Confirme se há espaço em disco
- Execute como administrador se necessário

## Dicas de Uso

1. **Organize por Status**: Use os filtros para visualizar apenas diligências pendentes
2. **Backup Regular**: Faça backups antes de grandes alterações
3. **Exportação Periódica**: Exporte dados mensalmente para Excel
4. **Observações Detalhadas**: Use o campo observações para informações importantes
5. **Controle Financeiro**: Mantenha os valores atualizados para relatórios precisos

## Suporte Técnico

Para suporte técnico:
1. Consulte os logs em `logs/diligencias_AAAAMMDD.log`
2. Execute o teste de sistema: `python tests/test_deploy.py`
3. Verifique a documentação técnica em `docs/README.md`

## Atualizações

O sistema verifica automaticamente por atualizações. Para atualizar manualmente:
1. Faça backup dos dados
2. Baixe a nova versão
3. Execute a instalação sobre a versão anterior
4. Os dados serão preservados automaticamente