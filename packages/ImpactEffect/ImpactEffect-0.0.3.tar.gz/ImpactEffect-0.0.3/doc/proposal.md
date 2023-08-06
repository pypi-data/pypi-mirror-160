# Proposal for Impact Effects

## Introduction

Our main goal is to rebuild a Python library based on the original code and thesis. It can provide necessary functions and expansion to build their own applications to simulate and observe the whole process of asteroids and comet impacts. Users can use it for experimental teaching, but also use the results it produced for scientific research. Some possible application directions, for example, use the results it produces to build a risk prediction tool, predict the possible impact of impact events, and so on. We will consider the necessary expansion, including the result of a web program to visualize the impact event, and use the Python library we built as the core. In addition, we plan to support the impact of the asteroid and the comet population on the target planet, because this situation is quite common.

## Background: Structure of original program

First, let's analyze the main logic of the original web program. After sorting out, we can extract key functions from it as the basis of implementing Python Library.

![overall](https://github.com/acse-dx121/impact-effects/blob/main/img/overall2.jpeg)

Web programs obtain data from the user input and check the effectiveness of the data. The IMPACT-EFFECT function affects the effect to calculate all the states and results, which contains a large number of sub-functions. The detailed logic of Impact-Effect is as follows:

**The main logic of impact_effects is:**

![](https://github.com/acse-dx121/impact-effects/blob/main/img/Flowchart.jpg)

As shown in the figure, the yellow part is the key function, and many important results are calculated using the formulas in the text. And if the box is wrapped in blue, that means that the function will print the relevant results.

Impact_effects overall logic is relatively simple, and gradually calculates related physical parameters.If the impact process meets some conditions, some additional calculation processes will be triggered.

### Drawbacks

In fact, the original code worked so well that the simulator quickly produced the results and displayed them on a web page. However, it still has some problems with our goals. 
- First, it is based on the scripting language Perl. Perl is a great language, but we wanted to build a tool that would be widely used. According to the most recent TIOBE data (May 2022), Perl ranks 17th in usage at less than one percent. Python ranks first at 12.74\%. This means that if we rebuild a library using Python, more users can save on the cost of learning the language. The audience will be much wider.
-  Second, the code structure can meet the requirements of building web applications, but it is strongly coupled. Strong coupling means that the main functions and variables in the program are bound together, which can cause a lot of trouble for subsequent extensions. A change in one variable may involve changes in several functions. Worse, however, are the references between variables and functions that are not shown. This is very unreadable code. 
- Third, the original code did not support modularity, nor did it support modern programming methods such as version control and continuous integration. This means that code quality cannot be guaranteed through continuous integration or benefit from modern automated deployment and testing tools. The lack of support for version control makes it difficult to work in groups during code development and to roll back code.

## ImpactEffect(Python Library) Design

### Objective

As some of the above problems exist, we consider using Python and modern programming techniques to build a usable and extensible Library while retaining the main functions of the original code. 
- We first want to use object-oriented programming ideas to organize our functions and data. The advantage of the object-oriented paradigm is that functions and data are bound together to simulate the real world in the form of an entity, such as an impactor, which we abstract as a class. The impactor class contains parameters that describe its properties, as well as necessary functions and methods. Similar logic applies to the target planet. So we can abstract the impact process, decouple it from the impactor and the impacted planet. 
- Second, we wanted to integrate version control and CI/CD so that we could continue to advance and evolve our projects. CI/CD supports automated validation and deployment of our code, reducing the probability of significant bugs. 
- In the end, we want the new Library to be easy to extend and easy to use, much of which depends on our code design.

### Design overview

![](https://github.com/acse-dx121/impact-effects/blob/main/img/pythonLibraryStructure.jpg)

Based on object-oriented ideas, we redesigned the entire program. The picture above shows the overall structure of IMPACTEFFECT. As shown in the figure, it is roughly divided into three modules:

### Function modules
The function module follows functional design, which contains all core calculation functions. Each function only accepts valuable parameters and returns the results of numericalization. When implementing, try to ensure the atomicity of the function, that is, there is no mutual dependence between functions. This atomic design makes the coupling of this part very low, which is conducive to subsequent expansion of new computing functions.

```python
def find_crater(p1, p2, p3):
    # ...
    return r1, r2, r3

def find_ejecta(p1, p2, p3):
    # ...
    return r1, r2, r3

###### etc...

```

### Impactor/ Impactor_Population/ Generator

We look forward to designing a reasonable structure in this part, which can describe both a single impactor and can describe a impactor population. Therefore, we need to design multiple classes to describe such a complex situation.

**Single Impactor**
We often consider this situation, that is, a single impactor hitting the target planet. Under such conditions, we only need to consider how to describe a single impactor. This is relatively simple, because a single parameter is not a distribution, so it can be represented by a value.
```python
class Impactor(Object):

    def __init__(p1, p2 ,...):
        self.p1 = p1
        self.p2 = p2
    
    def __getter__():
        return value
```

**Population of Impactor**
The situation is much more complicated for Population of Impactor. For Population of Impactor, the description of its parameters may be composed of multiple distributions. It is not a single hitter, but consists of many Impactors. Therefore, when we calculate the consequences of impact, it is unrealistic to use the distribution of parameters to calculate directly. Therefore, we need to use the sampling technology to select a series of specific impactors and use them to calculate the corresponding impact results. Impactor_population is used to describe their class.

```python
class Impactor_population(Object):
    def __init__():
        return

```

In order to achieve sampling, we first consider building a generator class. The Generator class represents all the values of a parameter. It can represent a distribution or a specific value.Generator provides a basic generate function to return all values. In general, the parameter of the IMPACTOR_POPULATION will be defined as such a type, and the IMPACT_POPULATION will also provide iterators to generate specific impacts.

```python
class Generator(Object):

```

In addition, the parameters of the impact may obey different distributions, so we need a class to describe different distributions. A common design idea is that the IMPACT_EFFECT package provides an abstract parent class that all distribution needs to inherit this parent class. Library provides common distribution implementation by default, such as Union distribution and Gaussion distribution.If users want to use a custom distribution, they need to inherit the Distribution class and implement relevant functions.

```python
class Distribution(Object):
    def __init__():
        return

class UnionDistribution(Distribution):
    def __init__():
        return
```

### Targets Class

Targets contains main functions and user interfaces. The parameters of the constructor are related parameters of the target planet transmitted by the user. Targets contains a series of important functional interfaces, such as Find_crater(). The user calls the interface and pass the instance of the Impactor/Impactor_Population as parameters. The interface is determined to pass the parameter type and perform different logic. If the passing parameter is impactor_population, then a MAP type is returned. The MAP key is the specific impactor, and the corresponding key value is the calculation result.The core calculation logic of the interface depends on Function Module.

```python
class Target(Object):
    def __init__():
        return

```


### User Case
In this part, we show how users use the basic features of IMPACT-EFFECT.
```python
import impactEffects

# single impactor
commet = impactEffects.Impactor(pdiameter = 100, .., type = commet)
target = impactEffects.Targets(tdense = 100, ...)
energy = target.find_energy(commet)

# the imapctor population
generator = impactEffects.Generator(is_range = false, Interval_left = 100, \
                            Interval_right = 10000, distribution = impactEffects.Union)

commets = impactEffects.Impactor_population(pdiameter = generator, p2 = )
target = impactEffects.Targets(tdense = 100, ...)
energyMap = target.find_energy(commets)

## get the result from energyMap
for key, val in energyMap:
    print("Imapctor: ", key, " val: ", val)

```

## Extension: [Web Application](https://github.com/acse-dx121/impact-effects-web)

![](https://github.com/acse-dx121/impact-effects/blob/main/img/webApp.jpeg)

### Objective
<!-- 在这一部分，我们计划设计一个现代Web应用程序，用于描述一个火山口的爆炸效果。我们的目标是构建一个可以自动化的撞击效果计算系统，并且可以可视化撞击结果。我们既希望可以模拟单一撞击器撞击效果，也希望可以模拟多个撞击器撞击效果。这样用户能够方便的模拟撞击效果，并且能够自动化的计算撞击结果。 -->

In this section, we plan to design a modern Web applications, is used to describe a effect of explosion crater Our goal is to build a can automate the impact effect of computing systems, and can be visual impact results We hope can simulate both the single impactor impact effect, also hope can simulate multiple impactor impact effect In this way, users can easily simulate the impact effect, and can automatically calculate the impact results. 

<!-- 从技术的角度来说，我们的应用应当能承载大规模的访问，以及做到防御一定程度的攻击，并且是非常容易部署的。 -->

From a technical point of view, our application should be able to host large-scale access, defend against a certain level of attack, and be very easy to deploy.

<!-- 对于单体应用来说，常见的部署方式是在服务器上运行一个进程，这个进程监听来自特定端口的请求。进程受到请求后，解析并进行处理。而这种方式的缺点是，如果服务器的负载过重，那么它就会受到大量的请求，这样就会导致服务器的压力增大。因为所有的请求都是有一个进程处理的。为了解决这个问题，我们时常会部署多个应用作为一个集群，这样就可以把大量的请求分发给每一个应用。分发操作由一个负载均衡器负责处理。另外引入docker技术，可以将应用的容器化，这样就可以让应用的部署更加灵活。用户可以很容易在本地运行服务。 -->

For single application, the common way of deployment is run on the server of a process, this process to monitor from a specific port request process by request, parse and processing And the shortcoming of this approach is, if the server load is overweight, so it will be a lot of request, this will cause the server's pressure Because all the request is a process to deal with In order to solve this problem, we often deploy multiple applications as a cluster, so that you can apply a large number of distributed to every request distribution operations by a load balancer is responsible for handling Also introduced docker technology, applications can be container, so that the application of deployment is more flexible Users can easily run services locally


### Design Details

<!-- 前端计划利用Vue框架进行实现。Vue是一个基于JavaScript的模板语言，它可以让我们在页面上进行渲染。Vue提供了很多组件，可以让我们方便的构建一个现代化的干净的界面。 -->

![](https://github.com/acse-dx121/impact-effects/blob/main/img/vue_temp.png)
**Fornt-end**
The front-end plan is implemented using Vue framework. Vue is a javascript-based templating language that lets you render on your page. Vue provides many components that make it easy to build a modern, clean interface.


<!-- 后端计划基于Flask实现。Flask是一个基于Python的Web框架。他虽然简单，但是提供了大部分我们需要的功能，比如路由、数据库、缓存等等。 -->
**Back-end**
The back-end plan is implemented based on Flask. Flask is a Python-based Web framework. It is simple, but it provides most of the functionality we need, such as routing, database, caching, and so on.

<!-- Docker技术用来容器化我们的Web应用，它能提供很好的应用隔离，并支持自动的大规模扩容以及应用重启。Docker-Compose技术用来管理我们的Docker容器集群，能够一键部署我们的应用。 -->
**Docker && Docker-Compose**
Docker technology is used to container our Web applications. It provides good application isolation and supports automatic mass scaling and application restart. Docker-compose technology is used to manage our Docker container cluster, enabling one-click deployment of our applications.