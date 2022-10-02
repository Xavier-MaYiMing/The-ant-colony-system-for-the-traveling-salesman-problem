### The ant colony system for the traveling salesman problem

##### Reference: Dorigo M, Gambardella L M.: Ant Colony System: A cooperative learning approach to the Traveling Salesman Problem. IEEE Tr. Evol. Comp. 1, 53-66[J]. 1997, 1(1): 53-66.

##### Reference: Dorigo M, Birattari M, Stutzle T. Ant colony optimization[J]. IEEE computational intelligence magazine, 2006, 1(4): 28-39.

| Variables  | Meaning                                                      |
| ---------- | ------------------------------------------------------------ |
| coord_x    | List, the x coordination of cities                           |
| coord_y    | List, the y coordination of cities                           |
| pop        | The number of ants                                           |
| iter       | The maximum number of iterations                             |
| alpha      | The pheromone decay parameter                                |
| beta       | The parameter which determines the relative importance of pheromone versus distance |
| rho        | The parameter for pheromone local updating rule              |
| q0         | The probability of exploitation versus exploration           |
| city_num   | The number of city                                           |
| dis        | List, dis\[i\]\[j\] denotes the distance between city i and city j |
| tau        | List, tau\[i\]\[j\] denotes the pheromone between city i and city j |
| start_city | List, start_city[i] denotes the start city of ant i          |
| iter_best  | List, the best so-far value of each iteration                |

#### Example

```python
if __name__ == '__main__':
    # Set the parameters
    pop = 20
    beta = 2
    q0 = 0.9
    alpha = 0.1
    rho = 0.1
    iter = 50
    city_num = 30
    min_coord = 0
    max_coord = 10
    coord_x = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    coord_y = [random.uniform(min_coord, max_coord) for _ in range(city_num)]
    print(main(coord_x, coord_y, pop, iter, alpha, beta, rho, q0))
```

##### Output:

![image]([https://github.com/Xavier-MaYiMing/The-ripple-spreading-algorithm-for-the-fuzzy-multi-objective-path-optimization-problem/blob/main/FMOPOP_example.PNG](https://github.com/Xavier-MaYiMing/The-ant-colony-system-for-the-traveling-salesman-problem/blob/main/convergence%20curve.png))

![image]([https://github.com/Xavier-MaYiMing/The-ripple-spreading-algorithm-for-the-fuzzy-multi-objective-path-optimization-problem/blob/main/FMOPOP_example.PNG](https://github.com/Xavier-MaYiMing/The-ant-colony-system-for-the-traveling-salesman-problem/blob/main/result.png))

```python
{
    'Best tour': [24, 1, 6, 9, 5, 7, 13, 19, 22, 12, 0, 28, 17, 18, 21, 16, 11, 23, 3, 27, 20, 10, 25, 14, 26, 2, 15, 4, 8, 29, 24], 
    'Shortest length': 48.85205394844219,
}

```

