---
marp: true
theme: rose-pine
size: 16:9
paginate: true
author: Adonai Arruda
title: Análise de dados para expansão de uma rede de laboratórios
header: Análise de dados para expansão de uma rede de laboratórios 

# criado com MARP: http://marp.app

style: |
    .columns {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
    }

    .columns > div:nth-child(2) img {
          
        max-width: 80%;  
        height: auto;    

        
        display: block;     
        margin-left: auto;  
        margin-right: auto; 
                            
        object-fit: contain; 
    }



    section {
        justify-content: flex-start !important;
        padding-top: 60px;
        padding-bottom: 80px;
        align-items: flex-start !important;
        text-align: left;
        position: relative;
    }

    .texto-menor { 
        font-size: 0.75em; 
    } 

    .contato-inferior-esquerdo {
        position: absolute !important;
        bottom: 40px;  /* Distância da borda inferior (ajuste o valor) */
        left: 60px;   /* Distância da borda esquerda (ajuste o valor) */
        width: auto;  /* Largura automática baseada no conteúdo */
    }

    /* Estilização opcional para a lista de contatos dentro do bloco */
    .contato-inferior-esquerdo ul {
        list-style: none; /* Remove bolinhas da lista */
        padding: 0;
        margin: 0;
    }

    .contato-inferior-esquerdo li {
    margin-bottom: 5px; /* Espaço entre o ícone/link do LinkedIn e o email */
    line-height: 1; /* Ajustar altura da linha se necessário */
    }

    /* Ajuste para o ícone do LinkedIn (se necessário) */
    .contato-inferior-esquerdo img {
    vertical-align: middle; /* Tenta alinhar verticalmente com texto, se houver */
    margin-right: 5px; /* Espaço à direita do ícone, se colocar texto ao lado */
    }

---

<!-- capa -->

# Análise de dados para expansão de uma rede de laboratórios

**Desenvolvido por:** Adonai Arruda
**Desenvolvido em:** Abril/2025

<div class="contato-inferior-esquerdo"><ul><li>
<a href="https://www.linkedin.com/in/adonai-arruda/" target="_blank">
  <img src="imgs/linkedin.png" alt="Linkedi" width="35" height="35">
</a>
<a href="mailto:joseadonai.jr@gmail.com">
  <img src="imgs/gmail.png" alt="Gmail" width="35">
</a>
<a href="[mailto:joseadonai.jr@gmail.com](https://github.com/adonaiarruda)">
  <img src="imgs/github.png" alt="Github" width="35">
</a>
</li></ul>
</div>



--- 

## Contextualização 

Uma rede de laboratórios pretende abrir novas filiais e necessita analisar regiões mais propícias para o empreendimento. 

A partir de dados transacionais das fmais de 100 filiais já em funcionamento, dados demográficos, geográficos e econômicos das regiões disponíveis para novas lojas, este estudo pretende realizar uma análise e indicar 3 potenciais regiões para implementação de uma ou mais filiais.  

--- 

## Bases de dados

### Fontes de Dados Utilizadas
* **Transacionais:** Registros de exames realizados por paciente e laboratório.
* **Exames:** Informações sobre os tipos de exame.
* **Geográficos:** Localização dos laboratórios (Lat/Long, ZCTA).
* **Econômicos:** Indicadores socioeconômicos agregados por ZCTA.
* **Demográficos:** Indicadores demográficos e populacionais agregados por ZCTA.


--- 

## Metodologia

1.  **Coleta:** Extração, limpeza e integração das 5 fontes de dados (Transacional, Exames, Geo, Econ, Demo).
2.  **Limpeza:** Tratamento de dados ausentes, duplicados e inconsistências.
3. **Hipóteses de negócio:** Definição de hipóteses a serem testadas.
4.  **Agregação:** Dados transacionais agregados por ZCTA, com contagem de exames e valores totais.
5.  **Análise Exploratória de Dados (EDA):** Geração de hipóteses sobre a natureza do problema e análise estatística para avaliar possíveis soluções e indicadores para avaliar as ZCTAs
6.  **Seleção da região:** Escolha fundamentada das 3 ZCTAs com maior destaque nos critérios definidos.


--- 

## Limpeza de dados

- Foi realizada limpeza e validação de dados individualmente em cada base de dados. As principais etapas foram:
* Na base de dados transacionais:
  *  Criação da variável `age_at_service` (idade do paciente na data do exame).
  *  Tratamento de outliers de idade (ex: > 160 anos) via _Winsorização_ na variável `age_at_service`.
  *  Padronização do formato decimal em 'Testing cost'

---

*  Na base de dados demográficos:
   *  Remoção de ZCTAs com menos de 10 habitantes nos dados demográficos
   *  Tratamento de outliers via _Winsorização_ em dados de proporção de gênero
   *  Imputação da mediana de idade em regiões sem estes dados


*  Na base de dados econômicos 
   *  Remoção de duplicatas
   *  Criação da variável de receita média `WeightedMeanIncome`
   *  Criação da variável de total de residências `TotalHouseholds`
  
* Na base de dados geográficos
  *  Transformação de código de área `Zipcode` para `ZCTA`

--- 

## Hipóteses de negócio

Foram elaboradas 5 hipóteses para serem analisadas:
1. Áreas com maior poder aquisitivo (renda familiar) têm maior potencial de lucro para os laboratórios.
2. Áreas com maior densidade populacional apresentam maior lucro para os laboratórios.
3. Áreas com população mais feminina apresentam maior demanda de serviços de laboratório.
4. Áreas com população mais idosa apresentam maior demanda de serviços de laboratório.
5. Áreas com mais de um laboratório apresentam menor lucro.

---

## Agregações

Os dados transacionais consistem na base de dados fundamental para obter as informções relevantes para responder às hipóteses elaboradas anteriormente. 

Combinando dados de exames e geográficos é possível obter:
- Lucro por exame
- Região que o laboratório se encontra

---



Combinando dados econômicos e demográficos, é possível obter informações sobre as regiões onde já existem laboratórios, como:
- Total de residências 
- Receita média por residência 
- População total
- Razão entre homens e mulheres da população 
- Mediana de idade da população 

Essas informações extraídas das bases são suficientes para responder as hipóteses de negócio criadas anteriormente.

---

<div class="columns">

<div> 

  ### Hipótese 1: 

  _Maior potencial aquisitivo = maior lucro_

  **Falso**

  <p class="texto-menor">
  A relação mostrada na figura ao lado mostra que, uma região mais rica (renda familiar média maior) não necessariamente se traduz em um maior lucro dos laboratório na região.
  </p>

</div>

<div>

![Relação Renda x Lucro](imgs/income-profit.png) 

</div>

</div>

---

<div class="columns">

<div> 

  ### Hipótese 2: 

  _Maior densidade populacional = maior lucro_

  **Verdadeiro**

  <p class="texto-menor">
  A relação mostrada na figura ao lado mostra que, laboratórios em regiões mais povoadas tendem a obter maior lucro.
  </p>

</div>

<div>

![Relação População x Lucro](imgs/population-profit.png) 

</div>

</div>

---

<div class="columns">

<div> 

  ### Hipótese 3: 

  _População mais feminina = maior demanda_

  **Falso**

  <p class="texto-menor">
    Não é possível perceber um padrão claro entre a razão de homens para mulheres e o total de serviços realizados, mesmo desconsidrando valores extremos.
  </p>

</div>

<div>

![Relação Gênero x Demanda](imgs/womans-demand.png) 

</div>

</div>


---

<div class="columns">

<div> 

  ### Hipótese 4: 

  _População mais idosa = maior demanda_

  **Falso**

  <p class="texto-menor">
    Não é possível perceber o efeito da idade média da região em relação a quantidade de serviços realizados.
  </p>

</div>

<div>

![Relação Idade x Demanda](imgs/age-demand.png) 

</div>

</div>


 ---

<div class="columns">

<div> 

  ### Hipótese 5: 

  _Mais laboratórios = menor lucro_

  **Inconclusivo**

  <p class="texto-menor">
    Não é possível perceber um padrão entre o número de laboratórios em uma região e o lucro da região. Porém, a quantidade de regiões com mais de um laboratório é pequena para tirar uma conclusão afirmativa sobre esta hipótese. É sugerido estudos futuros para se aprofundar nesta hipótese.
  </p>

</div>

<div>

![Relação Idade x Demanda](imgs/lab-profit.png) 

</div>

</div>


 ---



## Conclusão

<p class="texto-menor">
Baseado nas análises feitas anteriormente, é recomendada a implementação de novas filiis da rede de laboratórios em regiões (ZCTAs) com maior densidade populacional e que ainda não possuem laboratórios da rede em funcionamento.
</p>
<p class="texto-menor">
Conclui-se que a renda, gênero ou perfil etário de uma determinada região não influciam significativamente no lucro dos laboratórios de uma região, porém, a densidade populacional sim.
</p>

---

## Recomendação

**Desta forma os ZCTAs indicados são:**

- ZCTA5 77449
- ZCTA5 77494
- ZCTA5 11368



---

# **Obrigado!**

<div class="contato-inferior-esquerdo"><ul><li>
<a href="https://www.linkedin.com/in/adonai-arruda/" target="_blank">
  <img src="imgs/linkedin.png" alt="Linkedi" width="35" height="35">
</a>
<a href="mailto:joseadonai.jr@gmail.com">
  <img src="imgs/gmail.png" alt="Gmail" width="35">
</a>
<a href="[mailto:joseadonai.jr@gmail.com](https://github.com/adonaiarruda)">
  <img src="imgs/github.png" alt="Github" width="35">
</a>
</li></ul>
</div>

