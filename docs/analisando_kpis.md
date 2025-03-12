# Análise das colunas do arquivo CSV para confirmação da coerência das métricas do Revenue Management

Definição teórica das KPIs e seu relacionamento com as colunas do arquivo CSV:

**1. Ocupação:**

***Definição Teórica:** A ocupação é a porcentagem de quartos disponíveis que estão ocupados em um determinado período.
***Fórmula:** (Número de Quartos Ocupados / Número Total de Quartos)*100
***Colunas do CSV:**
    - `quartos_ocupados_dia`: Número de quartos ocupados em um determinado dia.
    - `total_quartos`: Número total de quartos disponíveis no hotel.
***Coerência:** **SIM**, as colunas `quartos_ocupados_dia` e `total_quartos` são coerentes com a definição teórica de ocupação. Elas fornecem os dados necessários para calcular a porcentagem de quartos ocupados em um determinado dia.

**2. ADR (Average Daily Rate):**

***Definição Teórica:** O ADR é a receita média gerada por cada quarto ocupado em um determinado período.
***Fórmula:** Receita Total de Quartos / Número de Quartos Ocupados
***Colunas do CSV:**
    - `receita_quartos_dia`: Receita total gerada pelos quartos em um determinado dia.
    - `quartos_ocupados_dia`: Número de quartos ocupados em um determinado dia.
***Coerência:** **SIM**, as colunas `receita_quartos_dia` e `quartos_ocupados_dia` são coerentes com a definição teórica de ADR. Elas fornecem os dados necessários para calcular a receita média por quarto ocupado em um determinado dia.

**3. RevPAR (Revenue Per Available Room):**

***Definição Teórica:** O RevPAR é a receita média gerada por cada quarto disponível no hotel em um determinado período.
***Fórmulas:**
    - Receita Total de Quartos / Número Total de Quartos
    - Ocupação*ADR
***Colunas do CSV:**
    - `receita_quartos_dia`: Receita total gerada pelos quartos em um determinado dia.
    - `total_quartos`: Número total de quartos disponíveis no hotel.
    - `Ocupacao`: (calculada a partir de `quartos_ocupados_dia` e `total_quartos`)
    - `ADR`: (calculado a partir de `receita_quartos_dia` e `quartos_ocupados_dia`)
***Coerência:** **SIM**, as colunas `receita_quartos_dia` e `total_quartos`, ou as colunas `Ocupacao` e `ADR`, são coerentes com a definição teórica de RevPAR. Elas fornecem os dados necessários para calcular a receita média por quarto disponível no hotel.

**4. TRevPAR (Total Revenue Per Available Room):**

***Definição Teórica:** O TRevPAR é a receita total gerada por cada quarto disponível no hotel em um determinado período, incluindo receitas de quartos e outras fontes (alimentos, bebidas, etc.).
***Fórmula:** Receita Total (Quartos + Outros) / Número Total de Quartos
***Colunas do CSV:**
    - `receita_total_dia`: Receita total gerada pelo hotel em um determinado dia, incluindo receitas de quartos e outras fontes.
    - `total_quartos`: Número total de quartos disponíveis no hotel.
***Coerência:** **SIM**, as colunas `receita_total_dia` e `total_quartos` são coerentes com a definição teórica de TRevPAR. Elas fornecem os dados necessários para calcular a receita total por quarto disponível no hotel.

**5. GOP (Gross Operating Profit):**

***Definição Teórica:** O GOP é o lucro operacional bruto do hotel, que é a receita total menos os custos operacionais.
***Fórmula:** Receita Total - Custos Operacionais
***Colunas do CSV:**
    - `lucro_operacional_bruto_dia`: Lucro operacional bruto do hotel em um determinado dia.
***Coerência:** **SIM**, a coluna `lucro_operacional_bruto_dia` é coerente com a definição teórica de GOP. Ela fornece o valor do lucro operacional bruto do hotel em um determinado dia.

**6. GOPPAR (Gross Operating Profit Per Available Room):**

***Definição Teórica:** O GOPPAR é o lucro operacional bruto gerado por cada quarto disponível no hotel em um determinado período.
***Fórmula:** Lucro Operacional Bruto / Número Total de Quartos
***Colunas do CSV:**
    - `goppar_dia`: Lucro operacional bruto por quarto disponível em um determinado dia.
***Coerência:** **SIM**, a coluna `goppar_dia` é coerente com a definição teórica de GOPPAR. Ela fornece o valor do lucro operacional bruto por quarto disponível em um determinado dia.

## **Objetivo das Metas:**

As barras de progresso podem representar três métricas-chave de Revenue Management:

    Meta 1: Taxa de Ocupação (Occupancy Rate)

        O que mede: A porcentagem de quartos ou unidades ocupadas em relação ao total disponível.

        Objetivo: Atingir uma taxa de ocupação ideal (por exemplo, 80%).

        Progresso: Se a ocupação atual for 50%, a barra mostrará 50% de progresso em relação ao objetivo de 80%.

        Cor: Verde ("success") se estiver acima de 70%, amarelo ("warning") se estiver entre 50% e 70%, e vermelho ("danger") se estiver abaixo de 50%.

    Meta 2: Receita por Unidade Disponível (RevPAR - Revenue per Available Room)

        O que mede: A receita gerada por quarto disponível, independentemente de estar ocupado ou não.

        Objetivo: Atingir um RevPAR de R$ 200, por exemplo.

        Progresso: Se o RevPAR atual for R140,abarramostraraˊ70140,abarramostraraˊ70 200.

        Cor: Verde se estiver acima de R180,amareloseestiverentreR180,amareloseestiverentreR 120 e R180,evermelhoseestiverabaixodeR180,evermelhoseestiverabaixodeR 120.

    Meta 3: Taxa de Conversão de Reservas (Booking Conversion Rate)

        O que mede: A porcentagem de visitantes do site ou plataforma que realizam uma reserva.

        Objetivo: Atingir uma taxa de conversão de 10%.

        Progresso: Se a taxa atual for 2,5%, a barra mostrará 25% de progresso em relação ao objetivo de 10%.

        Cor: Verde se estiver acima de 8%, amarelo se estiver entre 5% e 8%, e vermelho se estiver abaixo de 5%.

**Conclusão:**

As colunas do arquivo CSV e suas relações com as definições teóricas das métricas de Revenue Management estão COERENTES com o que preceitua a teoria das métricas.
