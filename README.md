# Linear Algebra - 2D Projection of 3D Cube

Authors: [**Gustavo Barroso Souza Cruz**](https://github.com/Gubscruz) & [**Henrique Turco Gera**](https://github.com/henriquetg1)

![](https://github.com/Gubscruz/3D-CUBE-PROJECTION/blob/main/3D_cube.gif)

## Como executar:
1. Acesse o diretório onde deseja clonar o repositório com o comando 
```cd /caminho/do/diretorio/```
2. Clone o repositório com o comando 
```git clone https://github.com/insper-classroom/aps4-henrique-t-gustavo-c.git```
3. Instale as dependências com o comando 
```pip install -r requirements.txt```
4. Execute o arquivo cube.py com o comando 
```python3 cube.py```

### Movimentação:
O programa permite que o usuário navegue pelo mundo 3D, como um jogo em primeira pessoa. Para se movimentar utilize as teclas:
- ```W```: Move para frente
- ```A```: Move para a esquerda
- ```S```: Move para trás
- ```D```: Move para a direita

---

## O Modelo Matemático:

### Representação do Cubo:
O cubo é representado por uma matriz 4x8 onde cada coluna representa um vértice do cubo em coordenadas homogêneas. A matriz é dada por:

$$ 
Cubo=\begin{bmatrix}
x_0 & x_1 & ... & x_7 \\
y_0 & y_1 & ... & y_7 \\
z_0 & z_1 & ... & z_7 \\
1 & 1 & ... & 1
\end{bmatrix}
$$

Essa representaçao foi escolhida para facilitar a multiplicação da matriz de projeção com a matriz do cubo.

### Rotacionando o Cubo:
Para rotacionar o cubo, utilizamos matrizes de rotação em torno dos eixos $x$, $y$ e $z$. A matriz de rotação em torno do eixo $x$ é dada por:

$$
R_x = \begin{bmatrix}
1 & 0 & 0 & 0\\
0 & \cos(\theta) & -\sin(\theta) & 0\\
0 & \sin(\theta) & \cos(\theta) & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

A matriz de rotação em torno do eixo $y$ é dada por:

$$
R_y = \begin{bmatrix}
\cos(\theta) & 0 & \sin(\theta) & 0\\
0 & 1 & 0 & 0\\
-\sin(\theta) & 0 & \cos(\theta) & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

E a matriz de rotação em torno do eixo $z$ é dada por:

$$
R_z = \begin{bmatrix}
\cos(\theta) & -\sin(\theta) & 0 & 0\\
\sin(\theta) & \cos(\theta) & 0 & 0\\
0 & 0 & 1 & 0\\
0 & 0 & 0 & 1
\end{bmatrix}
$$

Como o cubo já está na origem, podemos aplicar a rotação diretamente na matriz do cubo:

$$
R = R_z \cdot R_y \cdot R_x
$$

$$
Cubo_{rotacionado} = R \cdot Cubo
$$

obs: transladamos o cubo em 4 unidades em $z$ para que ele não fique em cima do pinhole (que fica em $z=0$)

---

### A Matriz de Projeção:

![](https://github.com/Gubscruz/3D-CUBE-PROJECTION/blob/main/pinhole_diagrama.png)

Observando os dois triângulos formados pela reta que liga o objeto (coordenadas $(x_0, z_0)$) ao ponto em que ela intersecta o plano de projeção (coordenadas $(x_p, z_p)$), notamos que eles têm dois ângulos correspondentes congruentes (o ângulo reto e o ângulo que representa o arco tangente do coeficiente angular da reta). Portanto, os triângulos são semelhantes, e, a partir disso podemos escrever que:
$$\frac{z_0}{x_0} = \frac{z_p}{x_p}$$
e, como $x_p = -d$, temos que:
$$x_p = -\frac{d \cdot x_0}{z_0}$$

note que $x_p$ não é uma combinação linear de $x_0$ e $z_0$, pois eles não são linearmente independentes. Para resolver este problema, reescrevemos a equação acima como:
$$x_0 = -\frac{z_p \cdot x_p}{d}$$

Além disso, vamos criar uma variável $w_p$ que dependa linearmente de $x_0$:
$$w_p = -\frac{z_0}{d}$$

Escrevemos dessa forma para que, enfim, possamos escrever $$x_0 = x_p \cdot w_p$$ a vantagem disso é que podemos achar os valores através de uma multiplicação matricial:

$$
\begin{bmatrix}
z_p \\
x_p \cdot w_p \\
w_p
\end{bmatrix} =
\begin{bmatrix}
0 & 0 & -d \\
1 & 0 & 0 \\
0 & -\frac{1}{d} & 0
\end{bmatrix} \cdot
\begin{bmatrix}
x_0 \\
z_0 \\
1
\end{bmatrix}
$$

similarmente, fazendo o memo processo para $y_p$:

$$
\begin{bmatrix}
z_p \\
y_{p}\cdot w_{p} \\
w_p \\
\end{bmatrix}= 
\begin{bmatrix}
0 & 0 & -d \\
1 & 0 & 0 \\
0 & -\frac{1}{d} & 0 \\
\end{bmatrix} \cdot
\begin{bmatrix}
y_o \\
z_o \\
1 \\
\end{bmatrix}
$$

combinando as duas transformações, e reorganizando a matriz escrevemos a matriz de projeção $P$:

$$
\begin{bmatrix}
x_p \cdot w_p \\
y_p \cdot w_p \\
z_p \\
w_p
\end{bmatrix} =
\begin{bmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & 0 & -d\\
0 & 0 & -\frac{1}{d} & 0
\end{bmatrix} \cdot
\begin{bmatrix}
x_0 \\
y_0 \\
z_0 \\
1
\end{bmatrix}
$$

onde

$$
\begin{bmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & 0 & -d\\
0 & 0 & -\frac{1}{d} & 0
\end{bmatrix} = P
$$

---

### Projetando o Cubo:
Para projetar o cubo, multiplicamos a matriz do cubo já rotacionado pela matriz de projeção:

$$
Cubo_{projetado} = P \cdot Cubo_{rotacionado}
$$

como ainda temos a matriz das coordenadas na representação que ainda depende do $w_p$, precisamos dividir cada coordenada pelo $w_p$ correspondente, normalizando a matriz: $(xw, yw, z, w) \implies (x, y, z/w)$ 

#### Escalando e Transladando para o centro:
Primeiro, excluimos o eixo $z$ da matriz do cubo projetado, pois ele não é relevante para a projeção. Em seguida, aplicamos a matriz de escala $S$ para tornar o cubo visível na tela, e a matriz de translação $T$ para centralizá-lo na tela:

$$
\begin{bmatrix}
x' \\
y' \\
1
\end{bmatrix} = T \cdot S \cdot
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
$$

onde

$$
T = \begin{bmatrix}
1 & 0 & \frac{WIDTH}{2} \\
0 & 1 & \frac{HEIGHT}{2} \\
0 & 0 & 1
\end{bmatrix}
$$

e

$$
S = \begin{bmatrix}
\frac{WIDTH}{2} & 0 & 0 \\
0 & \frac{HEIGHT}{2} & 0 \\
0 & 0 & 1
\end{bmatrix}
$$


#### Aplicando a Movimentação:
Para representar a movimentação lateral, somamos uma variável x_offset ao eixo x, transladando-o nesse eixo. Para representar a movimentação frontal, variamos a distância focal $d$ da matriz de projeção, alterando a distância entre o pinhole e o anteparo.

obs: como a distância focal não pode ser negativa (já que na matriz de projeção ela já é negativa, e, portanto, ficaria positiva, implicando que o anteparo estaria em frente ao pinhole), colocamos um limite que não permite que essa distância fique nula (evita divisão por zero) ou negativa

