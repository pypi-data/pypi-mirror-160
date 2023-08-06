# Proposal for Impact Effects

## Introduction

我们的主要目标是基于原始代码和论文重新构建一个python库，它能够提供必要的函和可拓展性给用户来构建他们自己的应用程序，用来模拟和观察小行星和彗星撞击的全过程。用户既可以用它来进行实验性的教学，又可以用它产生的结果进行科研研究。一些可能的应用方向例如，利用它产生的结果构建一个风险预测工具，预测撞击事件可能的影响等等。我们会考虑一下必要的拓展，包括一个web程序来可视化撞击事件的结果，利用我们构建的python库为核心。另外，我们计划支持小行星和彗星群对目标行星的撞击模拟，因为这种情况相当普遍。

## Background: Structure of original program

首先，我们分析一下原来的web程序的主要逻辑。在梳理之后，我们可以从中抽取出关键函数，作为后续实现python library的基础。

![overall](../img/overall2.jpeg)

Web程序从用户输入中获取数据，并检查数据的有效性。然后impact-effect函数影响效果计算所有的状态和结果，其中包含大量的子函数。impact-effect的详细逻辑如下: 

**The main logic of impact_effects is:**

![](../img/Flowchart.jpg)

如图所示，黄色部分是关键函数，利用文中的公式计算了许多重要的结果。而如果方框被蓝色包裹，代表会打印相关结果。

impact_effects整体逻辑比较简单，逐步计算相关的物理参数。如果撞击过程满足部分条件，则会触发额外的一些计算过程。

首先，程序计算能量..根据程序注释。

### Drawbacks

事实上，原始的代码工作地很好，模拟器能够迅速的给出模拟结果，并展示在网页上。但是，对于我们的目标而言，它仍旧存在一些问题。首先，他是基于脚本语言perl。perl语言非常优秀，但是我们希望构建的是一个能够广泛被使用的工具。根据TIOBE最新的数据（2022年五月），perl语言的使用占比小于百分之一，排名在第十七位。而python的使用占比在12.74%，排名第一。这意味着，如果我们使用python重新构建一个library，更多的用户可以省去学习语言的成本。受众将会更广。第二点，代码结构可以满足构建web应用的需求，但是它是强耦合的。强耦合意味着程序中主要函数和变量绑定在一起，这会对后续拓展造成极大的麻烦。一个变量的改动可能牵扯到多个函数的变动。然而更加糟糕的是，没有显示的变量和函数之间的引用关系。这非常不利于代码的阅读。第三点，原始的代码不支持模块化，也不支持版本控制和持续集成等现代编程方法。这意味着代码的质量难以通过持续集成来保证，也无法受益于现代自动化部署和测试工具。不支持版本控制使得代码拓展过程中很难进行团体合作，也很难进行代码回退。

## ImpactEffect(Python Library) Design

### Objective

正如上述一些问题存在，我们考虑使用python以及现代编程技巧，在保留原始代码的主要功能的情况下，构建出一个可用性强和拓展性强到Library。
- 首先希望利用面向对象编程的思想来组织我们的函数和数据。面向对象范式的优点在于讲函数和数据进行绑定，以实体的形式来模拟现实世界，例如对于撞击器来说，我们将其抽象为一个类。撞击器类包含有描述它本身性质的参数，以及一些必要的函数和方法。对于目标星球来说也是类似的逻辑。这样我们就可以将撞击过程抽象出来，它和撞击器以及被撞击星球解耦合了。
- 其次我们希望集成版本控制以及CI/CD，这样我们可以持续推进和演化我们的项目。CI/CD支持对我们的代码进行自动化校验和自动化部署，减少重大BUG出现的概率。
- 最后，我们希望新的Library是易于拓展和易于使用的，这很大程度上取决于我们的代码设计。

### Design Details

![](../img/pythonLibraryStructure.jpg)

基于面向对象的想法，我们重新设计了整个程序。上图显示了ImpactEffect的整体结构。如图所示，大致分为三个模块：

<details>
<summary><strong>Function modules</strong></summary>
函数模块内遵循函数式设计，包含了所有核心的计算函数。其中每一个函数，都只接受数值化的参数，并返回数值化的结果。实现的时候，要尽量保证函数的原子化，即函数之间不存在相互依赖关系。这样原子化的设计，使得这部分的耦合度非常低，有利于后续拓展新的计算函数。

```python
def find_crater(p1, p2, p3):
    # ...
    return r1, r2, r3

def find_ejecta(p1, p2, p3):
    # ...
    return r1, r2, r3

###### etc...

```
</details>

<details>
<summary><strong>Impactor/ Impactor_Population/ Generator</strong></summary>

我们期待在这一部分设计出合理的结构，既能描述单个撞击器也能描述一个撞击器分布。因此我们需要设计多个类来描述这样复杂的情况

**单一撞击器**
我们时常考虑这样的情况，即一个单一撞击器撞击目标星球的情况。在这样的条件下，我们只需要考虑如何描述单一撞击器。这较为简单，因为单一的参数不是可变的，因此可以用一个数值来表示。
```python
class Impactor(Object):

    def __init__(p1, p2 ,...):
        self.p1 = p1
        self.p2 = p2
    
    def __getter__():
        return value
```

**Population of Impactor**
对于Population of Impactor, 情况要复杂很多。对于population of Impactor来说，描述它参数可能是由多个分布构成的。它并不是一个单一的撞击器，而是由许多撞击器构成。因此，当我们计算撞击后果的时候，直接使用参数的分布来计算是不现实的。因此，我们需要利用采样技术来选择一系列的具体的撞击器，利用他们来计算相应的撞击结果。Impactor_population 是用来描述他们的类。

```python
class Impactor_population(Object):
    def __init__():
        return

```

为了实现采样，我们首先考虑构建一个Generator类. Generator类表示了一个参数的所有取值，它既可以表示一个分布，也可以表示一个具体的值。Generater 提供基本的generate函数来返回所有的值。总的来说，Impactor_population的参数会被定义为这样的类型，Impact_population也会提供迭代器函数来生成具体的撞击器。

```python
class Generator(Object):

```

另外，撞击器的参数可能服从不同的分布, 因此我们需要一个类来描述不同的分布。一种常见的设计思路是，Impact_effect包提供一个抽象父类，所有的分布需要继承这个父类。Library默认提供常见的分布实现，例如联合分布和正态分布等。用户如果想要使用自定义的分布，需要继承Distribution类，并实现相关函数。

```python
class Distribution(Object):
    def __init__():
        return

class UnionDistribution(Distribution):
    def __init__():
        return
```

</details>

<details>
<summary><strong>Targets Class</strong></summary>

Targets 包含主要功能以及用户接口。构造函数的参数为用户传入的关于目标星球的相关参数。Targets包含有一系列重要的函数接口，例如find_crater()等。用户调用接口，传入Impactor/Impactor_population的实例，接口通过判断传入的参数类型，执行不同的逻辑。如果传入参数是impactor_population，那么函数返回一个Map类型。 Map的键是具体的Impactor，对应的键值是计算结果。接口的核心计算逻辑依赖于Function Module。

```python
class Target(Object):
    def __init__():
        return

```

</details>


### User Case
在这一部分，我们展示了用户如何使用impact-effect的基本功能。
```python
import impactEffects

# single impactor
commet = impactEffects.Impactor(pdiameter = 100, .., type = commet)
target = impactEffects.Targets(tdense = 100, ...)
energy = target.find_energy(commet)

# the imapctor population
generator = impactEffects.Generator(is_range = True, Interval_left = 100, \
                            Interval_right = 10000, distribution = impactEffects.Union)
commets = impactEffects.Impactor_population(pdiameter = )
target = impactEffects.Targets(tdense = 100, ...)
energyMap = target.find_energy(commets)

## get the result from energyMap
for key, val in energyMap:
    print("Imapctor: ", key, " val: ", val)

```

## Web Application
