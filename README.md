# TheTool   
TheTool é uma aplicação de segurança informática realizada no âmbito da Unidade Curricular Linguagens de Programação Dinãmicas do Mestrado em Engenharia de Segurança Informatica do Instituto Politecnico de Beja.

Esta ferramenta possui as seguintes funcionalidades:
- portscan = efectua um varrimento aos portos abertos num segmento de rede e guarda em bdls 
- conn = verifica as ligações activas nesta maquina, guarda-as em bd e permite gerar graficos de ocurrencias
- chat = cria uma sala de conversação encriptada entre 2 elementos
- logprocessor = processa ficheiro auth.log e gera relatorios pdf
- report = cria relatorios em pdf da utilização das tools chat e portscan

## Instalação de dependencias

Utilize o [pip](https://pip.pypa.io/en/stable/) para instalar as dependecias necessárias.

```bash
pip install -r requirements.txt
```
## Utilização
```bash
python3 thetool.py [tool_a_executar]

[tool_a_executar]:
	portscan = efectua um varrimento aos portos abertos num segmento de rede e guarda em bdls 
	conn = verifica as ligações activas nesta maquina, guarda-as em bd e permite gerar graficos de ocurrencias
	chat = cria uma sala de conversação encriptada entre 2 elementos
	logprocessor = processa ficheiro auth.log e gera relatorios pdf
	report = cria relatorios em pdf da utilização das tools chat e portscan
```
