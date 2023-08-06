# small_tools
Repository composed by some small Python tools to validade strings, values and others so as to facilitate the coding process

Leia-me, isto é importante!


1. SUPORTADA A VERSÃO 3 DE PYTHON<br>
1.1. Instalado o Virtualenv<br><br>
2. ATENTO AOS REQUIREMENTS:<br>
2.1. para instalar através do terminal: "(.venv) pip install -r requirements-dev.txt"
<br><br>
3. DEFINIDO PEP-8 no flake8:<br>
3.1. Criar arquivo ".flake8"<br>
'''
[flake8]<br>
max-line-length=120<br>
exclude=.venv<br>
'''<br>
3.2. Rodar o teste no terminal: ".venv) flake8"<br><br>

4. ESTABELECIDO O SETUP.PY para o lanchamento da biblioteca própria<br>
4.1. Importado o código para o 'setup.py' de [renzon/tekton-micro](https://github.com/renzon/tekton-micro/blob/master/setup.py)<br>
4.2. Criado o setup.py no PyCharm, dentro da pasta princial '/small_tools'<br>
4.3. IMPORTANTE: Alteradas algumas configurações dentr do SETUP.PY, como nome, e classificação #Para ver classificação:
([Pypi-Classifiers](https://pypi.org/classifiers/))<br>
4.4. IMPORTANTE 2: Alterado o código __init__ da pyThon Package "libipythonpro":<br>
"""<br>
__ version __ = '0.1'<br>
"""<br>
4.5. Para a realização do teste do setup.py, foi criado um VENV na pasta principal do PycharmProjects.<br>
4.5.1. Utilize o comando "<.venv>pip install -e small_tools" que ele já vai localizar o setup.py<br>
<br>
5. FEITO O LANÇAMENTO DO PRIMEIRO RELEASE NO GITHUB<br>
5.1. No terminal, definda uma TAG para a última atualização com " _(.venv) git tag 0.1_ "<br>
5.2. Posteriormente, foi indicado a TAG para ser destacada no GITHUB com o cmdo " _(.venv) git pull --tags_ "<br>
5.3. Feito teste de intalação com o Package em VENV com o link fornecido pelo GITHUB: " _(.venv) pip install 
@github_link_do_release.zip _"
<br>
<br>
6. FEITA A CRIAÇÃO DO PACKAGE .DIST/libpythonpro-0.2.tar.gz E DISTRIBUIÇÃO NO PYPI:<br>
6.1. Primeiramente, criou-se o "MANIFEST.in" para informar que devem ser copiados o README.md e o LICENCE:<br>
>   MANIFEST.in <br>
    include README.md<br>
    include LICENCE<br>
    6.2. No terminal, escrever o código para a criação do package .DIST:" (.venv) python setup.py sdist "<br><br>
    6.3 Ainda no terminal, fazer o upload do arquivo:" (.venv) twine upload dist/* "<br><br>
    6.4 Após a instalação, colocar as credenciais do PYPI e verificar no site se tudo está funcionando

<br>
TOPICOS ABORDADOS:<br>
1. GIT
2. VIRTUALENV
3. PIP
4. Atento ao pull request
5. Trabalhando com o ".gitignore"
5.1. Adicionado "rascunho" no ".gitignore"
6. Realizar alguns PULLREQUEST e testá-los
7. Obter uma reprova no PULLREQUEST <br>
7.1. cuidado com o comando no terminal 'git reset --hard HEAD^1', pode causar problemas<br>
7.2. Por isso, o jeito mais adequado de se fazer é através do ... <br>
8. Realizado treinamento para a configuração de setpu.py para instalação de Packages e Libraries<br>
9. Realizado o primeiro release no [ramos-rr/small_tools/releases](https://github.com/ramos-rr/small_tools/releases)<br>
