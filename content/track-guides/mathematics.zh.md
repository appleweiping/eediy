## 四门基础课组成一张翻译桌，而不是四级台阶

[18.01SC](001-18-01sc.md)的[官方课程页](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/)处理单变量变化率与累积，[18.02SC](002-18-02sc.md)把它们带进多变量几何、向量场和积分，[18.03SC](003-18-03sc.md)把变化写成随时间演化的微分方程，[18.06SC](004-18-06sc.md)的[官方课程页](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/)则提供 vector space、linear map、least squares 与 eigenmode。EE 真正常用的是物理叙述、连续方程、矩阵与图形之间的翻译，不是四张按课程号排列的播放列表。第一次学习通常由 18.01SC 进入 18.02SC；基本积分稳定后即可并行 18.06SC，18.03SC 也不必等待全部多变量内容结束。公开 problem set 与 exam 应用于定位不会独立推导、画图或复核的单元，而不是证明视频已经看完。

## 后续工程对象决定 18.02、18.03 与 18.06 在哪里相遇

准备学电磁场时，把 18.02SC 的 gradient、divergence、line/surface integral 放在二维或三维势场上；准备学信号与控制时，把 18.03SC 的 linear ODE、Laplace transform 与 18.06SC 的 eigenvalue、orthogonal projection 放在同一状态方程上。可以用 2 阶 RLC 作纸笔检查：由元件关系写 ODE 与初值，再写 state matrix，求 eigenmode，并解释欠阻尼、临界阻尼和过阻尼在 time trace 与 eigenvalue plane 中为何一致。换成二维静电势时，则要先画积分区域、边界方向和单位，再离散成矩阵；basis 改变应改变坐标，不应改变物理解。

每次推导至少经过一个独立质询：量纲、极限、对称性、已知特例或小规模数值。symbolic software 可以化简，numerical library 可以求解，但不能由同一脚本同时制造基准和待检结果。若物理叙述写不出 initial/boundary condition，说明障碍不在矩阵算法；若线性算子能写成数组却解释不了 basis，18.06SC 仍未接通。数学能力在这些接口处显现，而不是在公式数量上显现。

## 18.04、18.065 与 6.055J 只处理已经出现的障碍

[18.04](005-18-04.md)适合 AC circuit、frequency-domain method 或二维场问题已经需要 residue、conformal map 与 harmonic function 的时候；它的公开材料没有 lecture video，脱离应用对象容易退化成符号技巧。[18.065](009-18-065.md)把线性代数推进 data、signal 和 optimization，不能替代 18.06SC 对空间与线性映射的基础训练；公开作业无解，final-project 材料也不完整，需要手算小例、独立实现和已知特例自检。[6.055J](018-6-055j.md)讲 dimension、scaling 与 approximation，最适合穿插在器件、传热或电路项目中。需要二维势函数才读 18.04，需要大矩阵与数据方法才读 18.065，需要数量级判断随时翻 6.055J；同时打开三门只会制造目录上的“进阶”。

## 同一个 EE 模型要给出解析、近似与数值三个版本

选择之后会复用的对象，例如 RLC、二维静电势、离散状态估计或热扩散。项目从物理假设与连续方程展开，给出矩阵表示、解析或半解析预测，以及可重复的数值实现；至少扫描三个尺度或参数区间，比较 condition number、discretization error 与近似的有效范围。若使用 complex variable 或 matrix method，说明它相对直接积分、time stepping 或 scalar calculation 解决了什么，并设计一个不适用的反例。

结果应允许读者从 plot 追到 equation、basis、boundary condition、参数与单位。最后保留一个解析近似开始失效的参数区间：先用 condition number、discretization error 或 residual 定位原因，再说明换 basis、细化网格或回到连续方程中的哪一步能够修正。这个反例比课程清单更清楚地显示数学表示何时足够、何时需要升级。
