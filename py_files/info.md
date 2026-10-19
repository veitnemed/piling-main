## ТЕСТ НА ПИЛЕНГОВАНИЕ КРУГОВОЙ РЕШЕТКОЙ АВП НИЗКОЧАСТОТНОГО ИЩЛУЧАТЕЛЯ МЕТОДАМИ БАРТЛЕТА, КЭЙПОНА И MUSIC 

# Акустический импеданс

<u>Акустический импеданс</u> в безграничной однородной атмосфере при $20^\circ\mathrm{C}$, скорости звука $c = 343{,}26\ \text{м/сек}$ и плотности воздуха $1{,}2041\ \text{кг/м}^3$ равен $z = 413{,}3\ \text{Па}\,\text{сек}/\text{м}$.


АВП - Акустический векторный приёмник 
## Круговая решётка АВП

Пусть $M$ обозначает количество датчиков, которые располагаются равномерно на окружности радиуса $R$. Начало системы координат решётки совпадает с центром окружности, ось $x$ проходит через первый по индексу датчик ($m = 1$). Оси всех АВП, неподвижных на решётке, ориентированы в одном направлении, именно вдоль оси $x$ системы координат. Азимут $\varphi_0 \in [0, 2\pi]$, под которым волна приходит на решётку, отсчитывается против часовой стрелки от оси $x$. Угол $\gamma_m$ между $m$-м датчиком и осью $x$ будет:

$$
\gamma_m = \frac{2\pi(m - 1)}{M}.
$$

Задержки прихода волны на датчики решётки отсчитываются относительно начала системы координат решётки:

$$
\tau_m = c^{-1}R\cos(\varphi_0 - \gamma_m).
$$

## Исходное уравнение АВП

$$
\begin{aligned}
y_0(t) &= P(t) + e_p(t), \\
y_{x_1}(t) &= z^{-1}P(t)\cos\varphi_0 + e_{x_1}(t), \\
y_{x_2}(t) &= z^{-1}P(t)\sin\varphi_0 + e_{x_2}(t).
\end{aligned}
$$

где $P(t)$ — детерминированный тестовый сигнал; $e_p(t)$, $e_{x_1}(t)$, $e_{x_2}(t)$ — независимые несмещённые гауссовы белые шумы в каналах АВП с дисперсиями $\sigma_p^2$, $\sigma_{x_1}^2$, $\sigma_{x_2}^2$.

## Тестовое уравнение АВП

Тестовое уравнение АВП получаем из исходного уравнения АВП, умножая его левую и правую части на $z$:

$$
\begin{aligned}
y_0(t) &= P(t) + e_p(t), \\
y_1(t) &= P(t)\cos\varphi_0 + e_1(t), & y_1(t) &= z y_{x_1}(t), & e_1(t) &= z e_{x_1}(t), \\
y_2(t) &= P(t)\sin\varphi_0 + e_2(t), & y_2(t) &= z y_{x_2}(t), & e_2(t) &= z e_{x_2}(t).
\end{aligned}
$$

## Тестовый сигнал

$$
P(t) = S(t), \qquad
S(t) =
\begin{cases}
A\sin\left(\dfrac{2\pi c}{\lambda}t\right), \\
\dfrac{A\tau}{\tau^2 + t^2}.
\end{cases}
$$

Считаем излучатель низкочастотным, если длина волны $\lambda_{\min}$, соответствующая верхней границе тестируемого диапазона частот, много больше геометрических размеров решётки:

$$
\frac{\lambda_{\min}}{2R} \geq 10.
$$

## Параметры тестирования

Относительные габариты решётки $\dfrac{\lambda_{\min}}{2R}$; $\lambda_{\min} = \lambda$ для гармонического тестового сигнала, $\lambda_{\min} = \lambda(\tau)$ для импульсного тестового сигнала, спектральная плотность которого равна $0{,}5A e^{-\lvert\omega\rvert\tau}$, $\omega = \dfrac{2\pi c}{\lambda}$; количество датчиков $M$; отношения сигнал/шум:

$$
\frac{A^2}{\sigma_p^2}, \qquad
\frac{A^2}{\sigma_{x_1}^2}, \qquad
\frac{A^2}{\sigma_{x_2}^2};
$$

среднеарифметическое значение оценок азимута каждым отдельным АВП.

## Выходные сигналы решётки АВП

$$
\begin{aligned}
y_0^{(m)}(t) &= P(t - \tau_m) + e_p^{(m)}(t), \\
y_1^{(m)}(t) &= P(t - \tau_m)\cos\varphi_0 + e_1^{(m)}(t), \qquad m = 1, \ldots, M, \quad t = 1, \ldots, N, \\
y_2^{(m)}(t) &= P(t - \tau_m)\sin\varphi_0 + e_2^{(m)}(t).
\end{aligned}
$$

Выборочная ковариационная матрица $\widetilde{\mathbf W}_{3M \times 3M}$ выходных сигналов решётки:

$$ 
\widetilde{\mathbf W} = \frac{1}{N}
\begin{bmatrix}
y_0^{(1)}(1) & y_0^{(1)}(2) & \cdots & y_0^{(1)}(N) \\
y_1^{(1)}(1) & y_1^{(1)}(2) & \cdots & y_1^{(1)}(N) \\
y_2^{(1)}(1) & y_2^{(1)}(2) & \cdots & y_2^{(1)}(N) \\
\vdots & \vdots & \ddots & \vdots \\
y_0^{(M)}(1) & y_0^{(M)}(2) & \cdots & y_0^{(M)}(N) \\
y_1^{(M)}(1) & y_1^{(M)}(2) & \cdots & y_1^{(M)}(N) \\
y_2^{(M)}(1) & y_2^{(M)}(2) & \cdots & y_2^{(M)}(N)
\end{bmatrix}
\begin{bmatrix}
y_0^{(1)}(1) & y_1^{(1)}(1) & y_2^{(1)}(1) & \cdots & y_0^{(M)}(1) & y_1^{(M)}(1) & y_2^{(M)}(1) \\
y_0^{(1)}(2) & y_1^{(1)}(2) & y_2^{(1)}(2) & \cdots & y_0^{(M)}(2) & y_1^{(M)}(2) & y_2^{(M)}(2) \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
y_0^{(1)}(N) & y_1^{(1)}(N) & y_2^{(1)}(N) & \cdots & y_0^{(M)}(N) & y_1^{(M)}(N) & y_2^{(M)}(N)
\end{bmatrix}.
$$

## Пространственные диаграммы направленности как функция угла $\varphi$

Введём вектор направления:

$$
\mathbf a(\varphi) =
\begin{bmatrix}
1 \\
\cos\varphi \\
\sin\varphi \\
\vdots \\
1 \\
\cos\varphi \\
\sin\varphi
\end{bmatrix}_{3M \times 1}.
$$

1. Бартлетт

$$
E_{\mathrm{BAR}}(\varphi) = \mathbf a^{\mathsf T}(\varphi)\,\widetilde{\mathbf W}\,\mathbf a(\varphi).
$$

2. Кэйпон

$$
E_{\mathrm{CAP}}(\varphi) = \frac{1}{\mathbf a^{\mathsf T}(\varphi)\,\widetilde{\mathbf W}^{-1}\,\mathbf a(\varphi)}.
$$

3. MUSIC

$$
\mathbf U = [\mathbf u_2\ \cdots\ \mathbf u_{3M}] = \operatorname{SVD}(\widetilde{\mathbf W}) \;/\; \text{набор $3M$-векторов}.
$$

$$
E_{\mathrm{MUS}}(\varphi) = \frac{1}{\mathbf a^{\mathsf T}(\varphi)\,\mathbf U\mathbf U^{\mathsf T}\,\mathbf a(\varphi)}.
$$

## Оценки искомого пеленга

1. Бартлетт: $\widehat{\varphi}_0 = \varphi_{\mathrm{BAR}} = \underset{\varphi}{\operatorname{arg\ max}}\ E_{\mathrm{BAR}}(\varphi)$.

2. Кэйпон: $\widehat{\varphi}_0 = \varphi_{\mathrm{CAP}} = \underset{\varphi}{\operatorname{arg\ max}}\ E_{\mathrm{CAP}}(\varphi)$.

3. MUSIC: $\widehat{\varphi}_0 = \varphi_{\mathrm{MUS}} = \underset{\varphi}{\operatorname{arg\ max}}\ E_{\mathrm{MUS}}(\varphi)$.
